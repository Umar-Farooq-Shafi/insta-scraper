# Django
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
import os
from django.conf import settings
import logging
from pathlib import Path
from decouple import config

logger = logging.getLogger('django')

# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.contrib import messages

def autologin(driver, url, username, password):
    driver.get(url)

    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
    )

    if password_input is not None:
        password_input.send_keys(password)
    else:
        print("Password input field not found.")

    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='text']"))
    )

    if username_input is not None:
        username_input.send_keys(username)
    else:
        print("Username input field not found.")

    form_element = password_input.find_element(By.XPATH, ".//ancestor::form")
    form_element.find_element(By.XPATH, ".//*[@type='submit']").click()
    
    return driver

def scrap(request):

    proj_dir = Path(settings.BASE_DIR).resolve().parent

    options = Options()
    # options.headless = True
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    driver.set_page_load_timeout(30)

    USERNAME = config("INSTA_USERNAME")
    PASSWORD = config("INSTA_PASSWORD")

    autologin(driver, 'https://www.instagram.com/accounts/login/', USERNAME, PASSWORD)

    timetable_popup = driver.find_element(By.XPATH, "//a[@href='javascript:timetable_popup();']").click()

    search_timetable = driver.find_element(By.XPATH, "//*[@id='sits_dialog']/center/div/div/div[3]/a").click()

    login_id = driver.find_element(By.XPATH, '//*[@id="poddatasection"]/div[2]/div[2]/div/div/fieldset/div[2]/label').get_attribute("for")
    login_id_modified = login_id.removesuffix('.1-1').replace(".", "_")
    login_id_truncated = login_id.removesuffix('.1-1')

    select_year_dropdown = driver.find_element(By.XPATH, "//*[@id='" + login_id_modified + "_1_1_chosen']/a").click()
    select_year = driver.find_element(By.XPATH, "//*[@id='" + login_id_truncated + ".1-111']").click()

    select_semester_dropdown = driver.find_element(By.XPATH, "//*[@id='" + login_id_modified + "_2_1_chosen']/a").click()
    select_semester = driver.find_element(By.XPATH, "//*[@id='" + login_id_truncated + ".2-120']").click()

    select_faculty_dropdown = driver.find_element(By.XPATH, "//*[@id='" + login_id_modified + "_3_1_chosen']/a").click()
    select_faculty = driver.find_element(By.XPATH, "//*[@id='" + login_id_truncated + ".3-121']").click()

    select_campus = Select(driver.find_element(By.ID, login_id.removesuffix('.1-1') + '.5-1'))
    select_campus.select_by_visible_text('UNIVERSITI MALAYA KUALA LUMPUR')

    submit_timetable = driver.find_element(By.XPATH, "//*[@id='poddatasection']/div[2]/div[3]/div/input[3]").click()

    last_page = driver.find_element(By.XPATH, "//*[@id='DataTables_Table_0_last']/a")
    driver.execute_script("arguments[0].click();", last_page)
    last_page_num = driver.find_element(By.XPATH, "//*[@id='DataTables_Table_0_paginate']/ul/li[7]/a").get_attribute('text')
    first_page = driver.find_element(By.XPATH, "//*[@id='DataTables_Table_0_first']/a")
    driver.execute_script("arguments[0].click();", first_page)
    table_element = driver.find_element(By.XPATH, "//*[@id='DataTables_Table_0_wrapper']")
    
    if not os.path.exists("maya.txt"):
        f = open("maya.txt", "a")
    else:
        f = open("maya.txt", "a")
    for i in range (int(last_page_num)):
        for tr in table_element.find_elements(By.TAG_NAME, 'tr'):

            if tr.get_attribute('class') == '' or tr.get_attribute('class') == None:
                f.write("PAGE " + str(i + 1) + "\n\n")
                f.write(tr.text)
            else:
                f.write(tr.text)

            f.write("\n\n")

        next_page = driver.find_element(By.XPATH, "//*[@id='DataTables_Table_0_next']/a")
        driver.execute_script("arguments[0].click();", next_page)

    f.close()

    driver.quit()
    messages.success(request, "Timetable extraction successful.")
    return HttpResponseRedirect('/main/')
