import logging
import random
import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from decouple import config
from .filter import PostFilter
from .post_parser import parse_explore
from .strategy import RunForeverStrategy
from .tracker import post_tracker

logging.basicConfig(handlers=[logging.StreamHandler()],
                    level=logging.INFO,
                    format='%(asctime)s [%(levelname).4s] %(message)s',
                    datefmt='%a %d %H:%M:%S')

logger = logging.getLogger('django')


class AutoLikeBot:
    def __init__(self, driver: WebDriver, post_filter, running_strategy):
        self.driver = driver
        self.post_filter = post_filter
        self.running_strategy = running_strategy

    def __enter__(self):
        self.log_in()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()
        logger.info(post_tracker.stats)
        return None

    def like_from_explore(self):
        max_id = 0

        while True:
            try:
                post = self.fetch_posts_from_explore()

                if self.post_filter.should_like(post):
                    self.like_post(post)

                    if not self.running_strategy.should_continue_run():
                        return
                else:
                    post_tracker.skipped_post(post)

            except TimeoutException:
                continue
                
            max_id += 1

    def log_in(self):
        self.driver.get("https://www.instagram.com/")

        USERNAME = config("INSTA_USERNAME")
        PASSWORD = config("INSTA_PASSWORD")

        try:
            self.wait_until(EC.presence_of_element_located((By.NAME, 'username')))

            try:
                self.driver.find_element(By.NAME, 'username').send_keys(USERNAME)

                password_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
                )

                password_input.send_keys(PASSWORD)

                form_element = password_input.find_element(By.XPATH, ".//ancestor::form")
                form_element.find_element(By.XPATH, ".//*[@type='submit']").click()

            except NoSuchElementException as e:
                logger.warning(f"Could not find element. Error: {e}")
                return

        except TimeoutException:
            pass

        try:
            # Remember this browser prompt
            self.driver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/section/div/button').click()
        except NoSuchElementException:
            pass

        try:
            # Turn on notifications prompt
            self.driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div/div[3]/button[2]").click()
            logger.debug("Skipping turn on notifications")
        except NoSuchElementException:
            pass

    def fetch_posts_from_explore(self):
        text = self.load_pre_from_url(f"https://www.instagram.com/reel/Ct-RoGKI9c7/")

        return parse_explore(text)

    def load_pre_from_url(self, url):
        self.open_and_switch_to_tab(url)
        try:
            like_path = '//*[@id="mount_0_0_He"]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/section[1]/div[1]/span[1]/div'

            self.wait_until(EC.presence_of_element_located((By.XPATH, like_path)), timeout=7)
            return self.driver.find_element(By.XPATH, like_path)
        finally:
            self.close_and_open_tab()

    # We will be opening tabs quite often so following methods will be used a lot
    def open_and_switch_to_tab(self, url):
        handles = self.driver.window_handles
        self.driver.execute_script(f"window.open('{url}');")
        # index based
        self.driver.switch_to.window(self.driver.window_handles[len(handles)])

    def close_and_open_tab(self, tab_index=0):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[tab_index])

    def like_post(self, post):

        self.open_and_switch_to_tab(post.post_link)
        try:
            self.wait_until(EC.presence_of_element_located((By.CLASS_NAME, 'fr66n')))
            self.driver.find_element(By.CLASS_NAME, 'fr66n').click()
            post_tracker.liked_post(post)
            logger.info(f"Liked {post}")
            time.sleep(rand_wait_sec())  # Replace rand_wait_sec with your actual random wait function
            return True

        # Post might get removed
        except (NoSuchElementException, TimeoutException):
            return False
        finally:
            self.close_and_open_tab()

    def wait_until(self, condition, timeout=5):
        WebDriverWait(self.driver, timeout).until(condition)
