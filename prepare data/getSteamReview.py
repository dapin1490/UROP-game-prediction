from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import pandas as pd

# steam web api doc : https://steamapi.xpaw.me/#IStoreService/GetAppList

# 게임 아이디 csv 불러오기
games = pd.read_csv("../UROP-game-prediction/prepare data/data/topSellerGames.csv")
games["review"] = None
revw = ""

chrome_driver = ChromeDriverManager().install()
service = Service(chrome_driver)

# reference : https://stackoverflow.com/questions/72758996/selenium-seleniumwire-unknown-error-cannot-determine-loading-status-from-unkn
# also reference : https://stackoverflow.com/questions/46920243/how-to-configure-chromedriver-to-initiate-chrome-browser-in-headless-mode-throug
# CHROMEDRIVER_PATH = r"C:\Users\dpgbu\.wdm\drivers\chromedriver\win32\103.0.5060.53\chromedriver.exe"
options = Options()
options.headless = True
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(1)

steamURL = "https://steamcommunity.com/app/"  # 기본 링크
reviewLink = "/reviews/?browsefilter=toprated&snr=1_5_100010_&filterLanguage=koreana"

total_num_game = len(games["appid"])

for i in range(0, total_num_game):  # 게임 아이디 수만큼 반복
    # steam 크롤링
    gid = games["appid"][i]
    revwURL = steamURL + str(gid) + reviewLink  # 게임 아이디로 상점 페이지 링크 생성
    print(f"i : {i}, lasts : {total_num_game - i}")
    print("ID :", gid)

    driver.get(revwURL)

    # 국가 제한 게임 여부 확인
    try:
        st = "#error_box"
        driver.find_element(By.CSS_SELECTOR, st)  # 이게 되면 게임 정보 수집 불가능
        revw = None
        continue
    except NoSuchElementException:
        pass

    # 성인 게임, 생년월일 입력 여부 판단
    # 참고 : https://codediary21.tistory.com/27
    # 참고 : https://ddang-goguma.tistory.com/35
    # /html/body/div[1]/div[7]/div[5]/div/div[2]/div/div[1]/div[3]/div/a[1]
    try:
        driver.find_element(By.CLASS_NAME, "agegate_birthday_selector")
        select = Select(driver.find_element(By.ID, "ageYear"))
        select.select_by_visible_text("1999")
        st = "#view_product_page_btn"
        driver.find_element(By.CSS_SELECTOR, st).click()
    except NoSuchElementException:
        pass

    try:
        driver.find_element(By.CSS_SELECTOR, "#age_gate_btn_continue").click()
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
    revw = res
    print(res)
    res = None
    
    games["review"].iloc[i:i + 1] = revw
    print(games.iloc[i:i + 1, :].transpose())
    
    print()  # 그냥 줄내림

    games.to_csv("../UROP-game-prediction/prepare data/data/topSellGameWReview.csv")
    print("progress saved\n")
# end of for