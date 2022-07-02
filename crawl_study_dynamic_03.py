from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

chrome_driver = ChromeDriverManager().install()
service = Service(chrome_driver)
driver = webdriver.Chrome(service=service)

steam_main = "https://store.steampowered.com/"
appid = 10
applink = steam_main + "/app/" + str(appid)
driver.get(applink)

time.sleep(2)

menu = driver.find_element(By.ID, "menuLink90")
menu.click()
time.sleep(1)

driver.switch_to.frame("cafe_main")
time.sleep(1)

xpath = "/html/body/div[1]/div/div[4]/table/tbody/tr[1]/td[1]/div[3]/div/a"

writing = driver.find_element(By.XPATH, xpath)
writing.click()
time.sleep(1)

content = driver.find_element(By.CSS_SELECTOR, "div.se-component-content").text
print(content)

driver.close()