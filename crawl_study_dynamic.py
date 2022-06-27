#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

chrome_driver = ChromeDriverManager().install()
service = Service(chrome_driver)
driver = webdriver.Chrome(service = service)

URL = "https://papago.naver.com/"
driver.get(URL)
time.sleep(5)

question = input("번역 할 영단어를 입력하세요 : ")

form = driver.find_element(By.CSS_SELECTOR, "textarea#txtSource")
form.send_keys(question)

button = driver.find_element(By.CSS_SELECTOR, "button#btnTranslate")
button.click()
time.sleep(2)

result = driver.find_element(By.CSS_SELECTOR, "div#txtTarget")
print(question, "->", result.text)

driver.close()