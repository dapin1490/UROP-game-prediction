from numpy import datetime_data
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
from datetime import datetime

def strDate_to_intDate(text):  # 영어 약어로 쓰인 month를 숫자로 반환
    if text == "Jan": return 1
    elif text == "Feb": return 2
    elif text == "Mar": return 3
    elif text == "Apr": return 4
    elif text == "May": return 5
    elif text == "Jun": return 6
    elif text == "Jul": return 7
    elif text == "Aug": return 8
    elif text == "Sep": return 9
    elif text == "Oct": return 10
    elif text == "Nov": return 11
    elif text == "Dec": return 12


# 게임 아이디 csv 불러오기
gameID = pd.read_csv("../UROP-game-prediction/prepare data/gameID.csv")
gameDates = []  # 출시 일자
prices = []  # 가격
devs = []  # 개발자
pubs = []  # 배급사
genre = []  # 장르
eacc = []  # '앞서 해보기' 여부
achiev = []  # 도전과제 유무
tag = []  # 태그
langs = []  # 지원 언어 수
stAward = []  # 스팀 어워드 수상 여부
dlcs = []  # DLC 유무

chrome_driver = ChromeDriverManager().install()
service = Service(chrome_driver)
driver = webdriver.Chrome(service=service)

steamURL = "https://store.steampowered.com/"  # 기본 링크

for i in range(len(gameID["appid"])):  # 게임 아이디 수만큼 반복
    gameURL = steamURL + "app/" + str(gameID["appid"][i])  # 게임 아이디로 상점 페이지 링크 생성
    print("i :", i, ", lasts :", 10000 - i)
    print("ID :", gameID["appid"][i])

    driver.get(gameURL)
    time.sleep(1)  # 페이지 로딩 대기 시간 1초

    # 국가 제한 게임 여부 확인
    try:
        st = "#error_box"
        driver.find_element(By.CSS_SELECTOR, st)  # 이게 되면 게임 정보 수집 불가능
        gameDates.append(None)
        prices.append(None)
        devs.append(None)
        pubs.append(None)
        genre.append(None)
        eacc.append(None)
        achiev.append(None)
        tag.append(None)
        langs.append(None)
        stAward.append(None)
        dlcs.append(None)
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
        driver.find_element(By.XPATH, '/html/body/div[1]/div[7]/div[5]/div/div[2]/div/div[1]/div[3]/div/a[1]').click()
        time.sleep(1)  # 페이지 로딩 대기 시간 1초
    except NoSuchElementException:
        pass

    # 출시 일자 수집
    # 리스트 gameDates
    try:
        result = driver.find_element(By.CSS_SELECTOR, "div.date").text.strip()
        # day month, year 형식으로 쓰임
        idx = result.find(" ")
        day = int(result[:idx])
        result = result[idx + 1:]
        month = strDate_to_intDate(result[0:3])
        year = int(result[5:])
        dday = datetime(year, month, day)  # 참고 : https://jsikim1.tistory.com/216
        print('date :', dday)
        gameDates.append(dday)
    except NoSuchElementException:
        gameDates.append(None)
    except:
        gameDates.append(None)
    
    # 가격 수집
    # 리스트 prices
    try:  # 정가 : div.game_purchase_action > div > div.game_purchase_price.price
        st = "div.game_purchase_action > div > div.game_purchase_price.price"
        res = driver.find_element(By.CSS_SELECTOR, st).text.strip()
        if res.find("Free") >= 0:  # 무료 게임은 0원
            res = "₩ 0"
        res = res[2:]
        res = res.replace(",", "")
        try:
            res = int(res)  # 가격을 int로 변환
        except ValueError:
            res = None
        prices.append(res)
        print("price :", res)
    except NoSuchElementException:
        try:  # 할인가 : div.game_purchase_action > div > div.discount_block.game_purchase_discount > div.discount_prices > div.discount_original_price
            res = driver.find_element(By.CSS_SELECTOR, "div.game_purchase_action div div.discount_block.game_purchase_discount div.discount_prices div.discount_original_price").text.strip()
            if res.find("Free") >= 0:  # 무료 게임은 0원
                res = "₩ 0"
            res = res[2:]
            res = res.replace(",", "")
            try:
                res = int(res)  # 가격을 int로 변환
            except ValueError:
                res = None
            prices.append(res)
            print("price :", res)
        except NoSuchElementException:
            prices.append(None)
            print("price : NULL")
    
    # 개발자 정보 수집
    # 리스트 devs
    try:  # 개발자가 여러 명 - 그 중 첫번째만 수집 : #developers_list > a:nth-child(1)
        res = driver.find_element(By.CSS_SELECTOR, "#developers_list > a:nth-child(1)").text.strip()
    except NoSuchElementException:  # 개발자 한 명 : #developers_list > a
        try:
            res = driver.find_element(By.CSS_SELECTOR, "#developers_list > a").text.strip()
        except NoSuchElementException:  # 이게 왜 없어..?
            res = None
    devs.append(res)
    print("developer :", res)
    
    # 배급사 정보 수집
    # 리스트 pubs
    try:  # 여러 명 중 첫 번째
        st = "#game_highlights > div.rightcol > div > div.glance_ctn_responsive_left > div:nth-child(4) > div.summary.column > a:nth-child(1)"
        res = driver.find_element(By.CSS_SELECTOR, st).text.strip()
    except NoSuchElementException:  # 한 명만
        try:
            st = "#game_highlights > div.rightcol > div > div.glance_ctn_responsive_left > div:nth-child(4) > div.summary.column > a"
            res = driver.find_element(By.CSS_SELECTOR, st).text.strip()
        except NoSuchElementException:  # 배급사 없음
            res = None
    pubs.append(res)
    print("publisher :", res)

    # 장르
    # 리스트 genre
    try:  # 여러 개
        st = "#genresAndManufacturer > span > a:nth-child(1)"
        res = driver.find_element(By.CSS_SELECTOR, st).text.strip()
    except NoSuchElementException:  # 1개
        try:
            st = "#genresAndManufacturer > span > a"
            res = driver.find_element(By.CSS_SELECTOR, st).text.strip()
        except NoSuchElementException:  # 장르 분류가 없는 게임도 있더라..
            res = None
    genre.append(res)
    print("genre :", res)

    # '앞서 해보기' 여부
    # 리스트 eacc
    st = "#genresAndManufacturer"
    try:
        res = driver.find_element(By.CSS_SELECTOR, st).text.strip()
        if res.find("EARLY ACCESS RELEASE DATE") >= 0:
            res = 1
        else:
            res = 0
        eacc.append(res)
    except NoSuchElementException:
        res = None
        eacc.append(res)
    print("early access :", res)

    # 도전과제 개수
    # 리스트 achiev
    st = "#achievement_block > div.communitylink_achievement_images > a"
    # "view /n all n" 형식으로 쓰임. n만 알아내면 됨
    try:
        res = driver.find_element(By.CSS_SELECTOR, st).text.strip()
        res = int(res[res.find("all") + 4:])
    except NoSuchElementException:  # 없으면 없는거지
        res = 0
    achiev.append(res)
    print("achievement :", res)

    # 인기 태그 1개
    # 리스트 tag
    st = "#glanceCtnResponsiveRight > div.glance_tags_ctn.popular_tags_ctn > div.glance_tags.popular_tags > a:nth-child(1)"
    try:
        res = driver.find_element(By.CSS_SELECTOR, st).text.strip()
    except NoSuchElementException:  # 혹시 없을까 해서 씀
        res = None
    tag.append(res)
    print("tag :", res)

    # 지원 언어 개수
    # 리스트 langs
    st = "#bannerLanguages > div.responsive_banner_link_title"
    try:
        res = driver.find_element(By.CSS_SELECTOR, st).get_attribute('innerText').strip()
        if res.find("and") >= 0:  # 반환된 텍스트에 "and"가 있으면 영어 이외 다른 언어를 더 지원하는 것이고
            res = int(res[res.find("and") + 4:res.find("more") - 1]) + 1
        else:  # "and"가 없으면 영어만 지원 / 어쨌든 한 가지 언어만 지원
            res = 1
    except NoSuchElementException:  # 못찾으면 결측값
        res = None
    langs.append(res)
    # print("languages :", res)

    # 스팀 어워드 수상 여부
    # 리스트 stAward
    st = "#awardsTable > div.block_content.block_content_inner"
    try:
        res = driver.find_element(By.CSS_SELECTOR, st).text.strip()
        if res.find("THE STEAM AWARDS") >= 0:  # 반환된 텍스트에 있으면 1
            res = 1
        else:  # 없으면 없는거지
            res = 0
    except NoSuchElementException:  # 이건 아예 수상 자체가 없는거니까 없는거지
        res = 0
    stAward.append(res)
    print("steam award :", res)

    # DLC 유무
    # 리스트 dlcs
    st = "#gameAreaDLCSection > div"
    try:  # 찾아서 나오면 있는거고
        res = driver.find_element(By.CSS_SELECTOR, st)
        res = 1
    except NoSuchElementException:  # 안나오면 없는거임
        res = 0
    dlcs.append(res)
    print("DLC :", res)

    print()  # 그냥 줄내림
# end of for

GDate = pd.DataFrame({
    "releaseDate": gameDates,
    "price": prices,
    "developer": devs,
    "publisher": pubs,
    "genre": genre,
    "early access": eacc,
    "achievement": achiev,
    "tag": tag,
    "languages":langs,
    "steam award": stAward,
    "DLC": dlcs
})

print(GDate.info())

games = pd.concat([gameID, GDate], ignore_index=True, axis=1)
games.to_csv("../UROP-game-prediction/prepare data/games.csv")
