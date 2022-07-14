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

# steam web api doc : https://steamapi.xpaw.me/#IStoreService/GetAppList

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
games02 = pd.read_csv("../UROP-game-prediction/prepare data/data/games_02.csv")
gameID = pd.read_csv("../UROP-game-prediction/prepare data/data/gameIDver02.csv")

thresh_cnt = int(len(games02.columns) * 0.8)
games02 = games02.dropna(thresh=thresh_cnt)
# print(games02.info())

chrome_driver = ChromeDriverManager().install()
service = Service(chrome_driver)

# reference : https://stackoverflow.com/questions/72758996/selenium-seleniumwire-unknown-error-cannot-determine-loading-status-from-unkn
# also reference : https://stackoverflow.com/questions/46920243/how-to-configure-chromedriver-to-initiate-chrome-browser-in-headless-mode-throug
# CHROMEDRIVER_PATH = r"C:\Users\dpgbu\.wdm\drivers\chromedriver\win32\103.0.5060.53\chromedriver.exe"
options = Options()
options.headless = True
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(1)

steamURL = "https://store.steampowered.com/"  # 기본 링크

total_num_of_games = len(gameID["appid"])

for i in range(838, total_num_of_games):  # 게임 아이디 수만큼 반복
    # steam 크롤링
    gameURL = steamURL + "app/" + str(gameID["appid"][i]) + "/"  # 게임 아이디로 상점 페이지 링크 생성
    print(f"i : {i}, lasts : {total_num_of_games - i}")
    print("ID :", gameID["appid"][i])

    driver.get(gameURL)

    # 국가 제한 게임 여부 확인
    try:
        st = "#error_box"
        driver.find_element(By.CSS_SELECTOR, st)  # 이게 되면 게임 정보 수집 불가능
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
        xpath = "/html/body/div[1]/div[7]/div[5]/div/div[2]/div/div[1]/div[4]/div/a[1]"
        driver.find_element(By.CSS_SELECTOR, st).click()
    except NoSuchElementException:
        pass

    # 게임 이름 수집
    # 리스트 gameName
    # name
    st = "#appHubAppName"
    try:
        res = driver.find_element(By.CSS_SELECTOR, st).text.strip()
    except NoSuchElementException:
        res = None
    name = res
    print(f"name : {res}")

    # 출시 일자 수집
    # 리스트 gameDates
    # date
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
        date = dday
    except NoSuchElementException:
        date = None
        print(f'date : {None}')
    except:
        date = None
        print(f'date : {None}')
    
    # 가격 수집
    # 리스트 prices
    # prc
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
        prc = res
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
            prc = res
            print("price :", res)
        except NoSuchElementException:
            prc = None
            print("price :", None)

    # 장르
    # 리스트 genre
    # gen
    try:  # 여러 개
        st = "#genresAndManufacturer > span > a:nth-child(1)"
        res = driver.find_element(By.CSS_SELECTOR, st).text.strip()
    except NoSuchElementException:  # 1개
        try:
            st = "#genresAndManufacturer > span > a"
            res = driver.find_element(By.CSS_SELECTOR, st).text.strip()
        except NoSuchElementException:  # 장르 분류가 없는 게임도 있더라..
            res = None
    gen = res
    print("genre :", res)

    # '앞서 해보기' 여부
    # 리스트 eacc
    # ea
    st = "#genresAndManufacturer"
    try:
        res = driver.find_element(By.CSS_SELECTOR, st).text.strip()
        if res.find("EARLY ACCESS RELEASE DATE") >= 0:
            res = 1
        else:
            res = 0
    except NoSuchElementException:
        res = None
    ea = res
    print("early access :", res)

    # 도전과제 개수
    # 리스트 achiev
    # ach
    st = "#achievement_block > div.communitylink_achievement_images > a"
    # "view /n all n" 형식으로 쓰임. n만 알아내면 됨
    try:
        res = driver.find_element(By.CSS_SELECTOR, st).text.strip()
        res = int(res[res.find("all") + 4:])
    except NoSuchElementException:  # 없으면 없는거지
        res = 0
    ach = res
    print("achievement :", res)

    # 인기 태그 1개
    # 리스트 tag
    # tg
    st = "#glanceCtnResponsiveRight > div.glance_tags_ctn.popular_tags_ctn > div.glance_tags.popular_tags > a:nth-child(1)"
    try:
        res = driver.find_element(By.CSS_SELECTOR, st).text.strip()
    except NoSuchElementException:  # 혹시 없을까 해서 씀
        res = None
    tg = res
    print("tag :", res)

    # 지원 언어 개수
    # 리스트 langs
    # lang
    st = "#bannerLanguages > div.responsive_banner_link_title"
    try:
        res = driver.find_element(By.CSS_SELECTOR, st).get_attribute('innerText').strip()
        if res.find("and") >= 0:  # 반환된 텍스트에 "and"가 있으면 영어 이외 다른 언어를 더 지원하는 것이고
            res = int(res[res.find("and") + 4:res.find("more") - 1]) + 1
        else:  # "and"가 없으면 영어만 지원 / 어쨌든 한 가지 언어만 지원
            res = 1
    except NoSuchElementException:  # 못찾으면 결측값
        res = None
    lang = res
    print("languages :", res)

    # 스팀 어워드 수상 여부
    # 리스트 stAward
    # stAw
    st = "#awardsTable > div.block_content.block_content_inner"
    try:
        res = driver.find_element(By.CSS_SELECTOR, st).text.strip()
        if res.find("THE STEAM AWARDS") >= 0:  # 반환된 텍스트에 있으면 1
            res = 1
        else:  # 없으면 없는거지
            res = 0
    except NoSuchElementException:  # 이건 아예 수상 자체가 없는거니까 없는거지
        res = 0
    stAw = res
    print("steam award :", res)

    # DLC 유무
    # 리스트 dlcs
    # dlc
    st = "#gameAreaDLCSection > div"
    try:  # 찾아서 나오면 있는거고
        res = driver.find_element(By.CSS_SELECTOR, st)
        res = 1
    except NoSuchElementException:  # 안나오면 없는거임
        res = 0
    dlc = res
    print("DLC :", res)

    # 모든 평가 긍정성
    # 리스트 allPositive
    # posiAll
    st = "#userReviews > div:nth-child(2) > div.subtitle.column.all"  # "All Reviews"
    try:
        res = driver.find_element(By.CSS_SELECTOR, st).text.strip().lower()
        if res.find("all") >= 0:
            st = "#userReviews > div:nth-child(2) > div.summary.column > span.game_review_summary.positive"
            try:
                res = driver.find_element(By.CSS_SELECTOR, st).text.strip().lower()
                if res.find("-") >= 0:
                    res = res[:res.find("-")].strip()
            except NoSuchElementException:
                res = None
        else:
            res = None
    except NoSuchElementException:
        st = "#userReviews > div > div.subtitle.column.all"  # "All Reviews"
        res = driver.find_element(By.CSS_SELECTOR, st).text.strip().lower()
        if res.find("all") >= 0:
            st = "#userReviews > div > div.summary.column"
            try:
                res = driver.find_element(By.CSS_SELECTOR, st).text.strip().lower()
                if res.find("-") >= 0:
                    res = res[:res.find("-")].strip()
            except NoSuchElementException:
                res = None
        else:
            res = None
    posiAll = res
    print("all posi :", res)

    # 최근 평가 긍정성
    # 리스트 last30dayPositive
    # posi30
    st = "#userReviews > div:nth-child(1) > div.subtitle.column"
    try:
        res = driver.find_element(By.CSS_SELECTOR, st).text.strip().lower()
        if res.find("recent") >= 0:
            st = "#userReviews > div:nth-child(1) > div.summary.column > span.game_review_summary.positive"
            try:
                res = driver.find_element(By.CSS_SELECTOR, st).text.strip().lower()
                if res.find("-") >= 0:
                    res = res[:res.find("-")].strip()
            except NoSuchElementException:
                res = None
        else:
            res = None
    except NoSuchElementException:
        res = None
    posi30 = res
    print("recent posi :", res)

    # 싱글/멀티 여부
    # 리스트 sing_or_mul
    # sORm
    sg = False
    mt = False
    st = "#category_block > div"
    try:
        res = driver.find_element(By.CSS_SELECTOR, st).text.strip()
        if res.find("Single-player") >= 0:
            sg = True
        if res.find("Co-op") >= 0:
            mt = True
    except NoSuchElementException:
        break
    
    if sg and mt:
        res = "single and multi"
    elif not sg and mt:
        res = "multi only"
    elif sg and not mt:
        res = "single only"
    else:
        res = None
    sORm = res
    print("is multi :", res)

    # 추천 리뷰 수
    # 리스트 posi_rev
    # posiRev
    st = "#reviews_filter_options > div:nth-child(1) > div.user_reviews_filter_menu_flyout > div > label:nth-child(5) > span"
    try:
        res = driver.find_element(By.CSS_SELECTOR, st).get_attribute('innerText').strip()
        res = res.replace(",", "")
        res = res.strip("(" ")")
        res = int(res)
    except NoSuchElementException:
        res = None
    posiRev = res
    print("posi review :", res)
    
    # 비추천 리뷰 수
    # 리스트 nega_rev
    # negaRev
    st = "#reviews_filter_options > div:nth-child(1) > div.user_reviews_filter_menu_flyout > div > label:nth-child(8) > span"
    try:
        res = driver.find_element(By.CSS_SELECTOR, st).get_attribute('innerText').strip()
        res = res.replace(",", "")
        res = res.strip("(" ")")
        res = int(res)
    except NoSuchElementException:
        res = None
    negaRev = res
    print("nega review :", res)

    # 개발자 정보 수집
    # 리스트 devs
    # dev
    # 팔로워 10만 이상 : 1
    # 팔로워 1만 이상 : 2
    # 팔로워 5천 이상 : 3
    # 팔로워 1천 이상 : 4
    # 팔로워 1천 미만 : 5
    # 확인할 수 없음 : 6
    try:  # 개발자가 여러 명 - 그 중 첫번째만 수집 : #developers_list > a:nth-child(1)
        res_button = driver.find_element(By.CSS_SELECTOR, "#developers_list > a:nth-child(1)")
        res_button.click()
        res = driver.find_element(By.CSS_SELECTOR, "div.num_followers").text.strip()
        res = res.replace(",", "")
        res = int(res)
    except NoSuchElementException:  # 개발자 한 명 : #developers_list > a
        try:
            res_button = driver.find_element(By.CSS_SELECTOR, "#developers_list > a")
            res_button.click()
            res = driver.find_element(By.CSS_SELECTOR, "div.num_followers").text.strip()
            res = res.replace(",", "")
            res = int(res)
        except NoSuchElementException:  # 팔로워를 확인할 수 없는 경우
            res = None
    
    if res != None:
        if res >= 100000:
            res = 1
        elif res >= 10000:
            res = 2
        elif res >= 5000:
            res = 3
        elif res >= 1000:
            res = 4
        else:
            res = 5
    else:
        res = 6
    dev = res
    print("developer tier :", res)

    while True:
        try:
            driver.get(gameURL)
            break
        except:
            continue

    # 성인 게임, 생년월일 입력 여부 판단
    # 참고 : https://codediary21.tistory.com/27
    # 참고 : https://ddang-goguma.tistory.com/35
    # /html/body/div[1]/div[7]/div[5]/div/div[2]/div/div[1]/div[3]/div/a[1]
    try:
        driver.find_element(By.CLASS_NAME, "agegate_birthday_selector")
        select = Select(driver.find_element(By.ID, "ageYear"))
        select.select_by_visible_text("1999")
        st = "#view_product_page_btn"
        xpath = "/html/body/div[1]/div[7]/div[5]/div/div[2]/div/div[1]/div[4]/div/a[1]"
        driver.find_element(By.CSS_SELECTOR, st).click()
    except NoSuchElementException:
        pass
    
    # 배급사 정보 수집
    # 리스트 pubs
    # pub
    # 팔로워 50만 이상 : 1
    # 팔로워 10만 이상 : 2
    # 팔로워 5만 이상 : 3
    # 팔로워 5천 이상 : 4
    # 팔로워 1천 미만 : 5
    # 확인할 수 없음 : 6
    try:  # 여러 명 중 첫 번째
        st = "#game_highlights > div.rightcol > div > div.glance_ctn_responsive_left > div:nth-child(4) > div.summary.column > a:nth-child(1)"
        res_button = driver.find_element(By.CSS_SELECTOR, st)
        res_button.click()
        res = driver.find_element(By.CSS_SELECTOR, "div.num_followers").text.strip()
        res = res.replace(",", "")
        res = int(res)
    except NoSuchElementException:  # 한 명만
        try:
            st = "#game_highlights > div.rightcol > div > div.glance_ctn_responsive_left > div:nth-child(4) > div.summary.column > a"
            res_button = driver.find_element(By.CSS_SELECTOR, st)
            res_button.click()
            res = driver.find_element(By.CSS_SELECTOR, "div.num_followers").text.strip()
            res = res.replace(",", "")
            res = int(res)
        except NoSuchElementException:  # 배급사 없음
            res = None
    
    if res != None:
        if res >= 100000:
            res = 1
        elif res >= 10000:
            res = 2
        elif res >= 5000:
            res = 3
        elif res >= 1000:
            res = 4
        else:
            res = 5
    else:
        res = 6
    pub = res
    print("publisher tier :", res)

    driver.get(gameURL)

    # 성인 게임, 생년월일 입력 여부 판단
    # 참고 : https://codediary21.tistory.com/27
    # 참고 : https://ddang-goguma.tistory.com/35
    # /html/body/div[1]/div[7]/div[5]/div/div[2]/div/div[1]/div[3]/div/a[1]
    try:
        driver.find_element(By.CLASS_NAME, "agegate_birthday_selector")
        select = Select(driver.find_element(By.ID, "ageYear"))
        select.select_by_visible_text("1999")
        st = "#view_product_page_btn"
        xpath = "/html/body/div[1]/div[7]/div[5]/div/div[2]/div/div[1]/div[4]/div/a[1]"
        driver.find_element(By.CSS_SELECTOR, st).click()
    except NoSuchElementException:
        pass

    # 도전과제 달성 최대 비율
    # 리스트 most_achiv_rate
    # mostAch
    # 개발자 라이브가 켜져 있는 경우
    try:
        # xpath = '//*[@id="game_highlights"]/div[1]/div/div[1]/div[1]/text()'
        # close_live = driver.find_element(By.XPATH, xpath)
        xpath = '//*[@id="game_highlights"]/div[1]/div/div[1]/div[1]/div[2]/div'
        close_live = driver.find_element(By.XPATH, xpath)
        close_live.click()
    except:
        pass

    st = "#achievement_block > div.communitylink_achievement_images > a"
    try:
        res_button = driver.find_element(By.CSS_SELECTOR, st)
        res_button.click()
        st = "#mainContents > div:nth-child(4) > div.achieveTxtHolder > div.achievePercent"
        res = driver.find_element(By.CSS_SELECTOR, st).text.strip()
        res = res.replace("%", "")
        res = float(res)
    except:  # 없으면 없는거임
        res = None
    mostAch = res
    print("most achiv rate :", res)

    # steam에서 더 수집할 데이터
    # 전체 플레이어 평균 도전과제 달성률
    # 스팀 게임 리뷰 데이터

    # steamcharts 크롤링
    steamchartsURL = "https://steamcharts.com/app/" + str(gameID["appid"][i])
    driver.get(steamchartsURL)

    # 최근 30일 동시 플레이어 수
    # 리스트 recent_player
    # rectplay
    st = "#content-wrapper > div:nth-child(7) > table > tbody > tr:nth-child(1) > td.right.num-f.italic"
    try:
        res = driver.find_element(By.CSS_SELECTOR, st).text.strip()
        res = res.replace(",", "")
        res = float(res)
    except NoSuchElementException:
        res = None
    rectplay = res
    print("recent player :", res)
    
    # 최다 동시 플레이어 수
    # 리스트 peek_player
    # peekpl
    st = "#app-heading > div:nth-child(4) > span"
    try:
        res = driver.find_element(By.CSS_SELECTOR, st).text.strip()
        res = res.replace(",", "")
        res = int(res)
    except NoSuchElementException:
        res = None
    peekpl = res
    print("peek player :", res)

    print()  # 그냥 줄내림
    # if i >= 3:
    #     break

    oneGame = pd.DataFrame({
        "appid": [gameID["appid"][i]],
        "title": [name],
        "releaseDate": [date],
        "price": [prc],
        "developer tier": [dev],
        "publisher tier": [pub],
        "genre": [gen],
        "early access": [ea],
        "achievement": [ach],
        "tag": [tg],
        "languages": [lang],
        "steam award": [stAw],
        "DLC": [dlc],
        "recent positive": [posi30],
        "all positive": [posiAll],
        "single or multi": [sORm],
        "positive review": [posiRev],
        "negative review": [negaRev],
        "recent player": [rectplay],
        "peek player": [peekpl],
        "most achieved rate": [mostAch]
    })

    games02 = pd.concat([games02, oneGame], ignore_index = True)
    games02 = games02.reset_index(drop=True)

    try:
        games02.drop('Unnamed: 0', axis=1, inplace=True)
    except:
        pass

    # print(games02.info())
    # print(games02.tail().transpose())

    games02.to_csv("../UROP-game-prediction/prepare data/data/games_02.csv")

    print("progress saved\n")
# end of for

