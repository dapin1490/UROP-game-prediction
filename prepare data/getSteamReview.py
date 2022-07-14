from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from datetime import datetime

# steam web api doc : https://steamapi.xpaw.me/#IStoreService/GetAppList

# 게임 아이디 csv 불러오기
games = pd.read_csv("../UROP-game-prediction/prepare data/data/games.csv")
revw = []

# chrome_driver = ChromeDriverManager().install()
# service = Service(chrome_driver)

# reference : https://stackoverflow.com/questions/72758996/selenium-seleniumwire-unknown-error-cannot-determine-loading-status-from-unkn
# also reference : https://stackoverflow.com/questions/46920243/how-to-configure-chromedriver-to-initiate-chrome-browser-in-headless-mode-throug
CHROMEDRIVER_PATH = r"C:\Users\dpgbu\.wdm\drivers\chromedriver\win32\103.0.5060.53\chromedriver.exe"
options = Options()
options.headless = True
driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)
driver.implicitly_wait(1)

steamURL = "https://steamcommunity.com/app/"  # 기본 링크
reviewLink = "/reviews/?browsefilter=toprated&snr=1_5_100010_&filterLanguage=koreana"

for i in range(0, len(games["appid"])):  # 게임 아이디 수만큼 반복
    # steam 크롤링
    revwURL = steamURL + str(games["appid"][i]) + reviewLink  # 게임 아이디로 상점 페이지 링크 생성
    print("i :", i, ", lasts :", 1000 - i)
    print("ID :", games["appid"][i])

    while True:
        try:
            driver.get(revwURL)
            break
        except:
            continue

    # 국가 제한 게임 여부 확인
    try:
        st = "#error_box"
        driver.find_element(By.CSS_SELECTOR, st)  # 이게 되면 게임 정보 수집 불가능
        revw.append(None)
        continue
    except NoSuchElementException:
        pass

    # 성인 게임, 생년월일 입력 여부 판단
    # 참고 : https://codediary21.tistory.com/27
    # 참고 : https://ddang-goguma.tistory.com/35
    # /html/body/div[1]/div[7]/div[5]/div/div[2]/div/div[1]/div[3]/div/a[1]
    try:
        st = "#age_gate_btn_continue"
        driver.find_element(By.CSS_SELECTOR, st).click()
    except NoSuchElementException:
        pass

    # 한국어 리뷰 수집
    # 리스트 revw
    st = "div:nth-child(2) > div.apphub_CardContentMain > div.apphub_UserReviewCardContent > div.apphub_CardTextContent"
    posted = "div:nth-child(2) > div.apphub_CardContentMain > div.apphub_UserReviewCardContent > div.apphub_CardTextContent > div"
    try:
        res = driver.find_element(By.CSS_SELECTOR, st).text.strip()
        pos = driver.find_element(By.CSS_SELECTOR, posted).text.strip()
        if res.find(pos) >= 0:
            res = res[res.find(pos) + len(pos) + 1:]
    except NoSuchElementException:
        res = None
    except:
        res = None
    revw.append(res)
    print(res)
    res = None

    print()  # 그냥 줄내림
    # if i >= 3:
    #     break

    GRevw = pd.DataFrame({
        "review": revw
    })

    # print(GRevw.info())

    gameWRevw = pd.concat([games, GRevw], axis=1)
    gameWRevw = gameWRevw.reset_index(drop=True)
    # print(gameWRevw.info())
    # print(gameWRevw.head())

    gameWRevw.drop('Unnamed: 0', axis=1, inplace=True)
    # print(gameWRevw.info())
    # print(gameWRevw.head())

    gameWRevw.to_csv("../UROP-game-prediction/prepare data/data/gameWReview.csv")
    print("progress saved\n")

    if i >= 515:
        break
# end of for

GRevw = pd.DataFrame({
    "review": revw
})

# print(GRevw.info())

gameWRevw = pd.concat([games, GRevw], axis=1)
gameWRevw = gameWRevw.reset_index(drop=True)
# print(gameWRevw.info())
# print(gameWRevw.head())

gameWRevw.drop('Unnamed: 0', axis=1, inplace=True)
# print(gameWRevw.info())
# print(gameWRevw.head())

gameWRevw.to_csv("../UROP-game-prediction/prepare data/data/gameWReview.csv")
# print("progress saved\n")