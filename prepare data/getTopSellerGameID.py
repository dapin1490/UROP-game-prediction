from tkinter.messagebox import NO
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import pandas as pd
from datetime import datetime
import time
from selenium.webdriver.common.keys import Keys

# 게임 아이디
gameID = []
isTopSeller = []

chrome_driver = ChromeDriverManager().install()
service = Service(chrome_driver)

# reference : https://stackoverflow.com/questions/72758996/selenium-seleniumwire-unknown-error-cannot-determine-loading-status-from-unkn
# also reference : https://stackoverflow.com/questions/46920243/how-to-configure-chromedriver-to-initiate-chrome-browser-in-headless-mode-throug
# CHROMEDRIVER_PATH = r"C:\Users\dpgbu\.wdm\drivers\chromedriver\win32\103.0.5060.53\chromedriver.exe"
options = Options()
options.headless = True
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(1)

steamURL = "https://store.steampowered.com/search/?sort_by=Reviews_DESC&category1=998&os=win&filter=topsellers"  # 기본 링크
driver.get(steamURL)

total_num_of_games = 500

for i in range(49, total_num_of_games + 1):  # 게임 아이디 수만큼 반복
    # steam 크롤링
    print("i :", i, ", lasts :", total_num_of_games - i)

    st = "#search_resultsRows > a:nth-child(" + str(i) + ")"

    # 게임 ID
    # 리스트 gameID
    try:
        res = driver.find_element(By.CSS_SELECTOR, st).get_attribute('href').strip()
        print(f"href : {res}")
        if res.find("app") < 0:
            continue
        res = res[res.find("app") + 4:]
        res = res[:res.find("/")]
        res = int(res)
    except NoSuchElementException:
        res = None
    gameID.append(res)
    isTopSeller.append(1)
    print(f"ID : {res}")

    if i % 50 == 0:
        body = driver.find_element(By.CSS_SELECTOR, 'body')
        body.send_keys(Keys.END)
        time.sleep(2)

    print()  # 그냥 줄내림
    # if i >= 3:
    #     break

    gameID_topSeller = pd.DataFrame({"appid": gameID, "is_top_seller": isTopSeller})
    gameID_topSeller.to_csv("../UROP-game-prediction/prepare data/data/topSellerGameID.csv")

    print("progress saved\n")
# end of for
