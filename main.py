from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome(executable_path="/Users/dev/Downloads/muneeb/chromedriver")
browser.implicitly_wait(5)

browser.get('https://www.instagram.com/')
login_link = browser.find_element(By.XPATH, "//div[text()='Log in']")
login_link.click()

sleep(2)

username_input = browser.find_element(By.XPATH, "input[name='username']")
password_input = browser.find_element(By.XPATH, "input[name='password']")

username_input.send_keys("<your username>")
password_input.send_keys("<your password>")

login_button = browser.find_element(By.XPATH, "//button[@type='submit']")
login_button.click()

sleep(5)

browser.close()