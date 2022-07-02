from selenium import webdriver  # 웹페이지를 조작하는 데 필요한 드라이버
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  # 웹드라이버 중 크롬 브라우저용 드라이버
from selenium.webdriver.common.by import By
import time
import pandas as pd

def new_driver():
    chrome_driver = ChromeDriverManager().install()  # 크롬 드라이버 받기
    service = Service(chrome_driver)  # 받은 드라이버로 서비스 객체 생성
    driver = webdriver.Chrome(service = service)  # 생성한 서비스 객체를 웹드라이버의 크롬에 전달
    return driver

driver = new_driver()

URL = "https://papago.naver.com/"
driver.get(URL)  # 웹페이지 접근
time.sleep(3)  # 페이지 로딩을 기다리기 위해 지연시간 부여

dict = pd.DataFrame({
    "word": [],
    "Kor": []
})

idx = 0

while True:
    question = input("번역 할 영단어를 입력하세요 : ")
    if question == "0":
        break
    if dict["word"].isin([question]).any():
        print("중복 입력")
        print(question, "->", dict["Kor"].where(dict["word"] == question))
        continue

    form = driver.find_element(By.CSS_SELECTOR, "textarea#txtSource")  # 번역할 텍스트 입력 블록
    form.send_keys(question)

    button = driver.find_element(By.CSS_SELECTOR, "button#btnTranslate")  # 번역 버튼
    button.click()
    time.sleep(2)  # 번역 결과 기다림

    result = driver.find_element(By.CSS_SELECTOR, "div#txtTarget")  # 번역 결과 텍스트 블록
    print(question, "->", result.text)
    dict.loc[idx] = [question, result.text]
    idx += 1

    form.clear()  # 요소의 내용 초기화
    time.sleep(3)

driver.close()  # 웹페이지 끄기