from selenium import webdriver  # 웹페이지를 조작하는 데 필요한 드라이버
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  # 웹드라이버 중 크롬 브라우저용 드라이버
from selenium.webdriver.common.by import By
import time

chrome_driver = ChromeDriverManager().install()  # 크롬 드라이버 받기
service = Service(chrome_driver)  # 받은 드라이버로 서비스 객체 생성
driver = webdriver.Chrome(service = service)  # 생성한 서비스 객체를 웹드라이버의 크롬에 전달

URL = "https://papago.naver.com/"
driver.get(URL)  # 웹페이지 접근
time.sleep(3)  # 페이지 로딩을 기다리기 위해 지연시간 부여

question = input("번역 할 영단어를 입력하세요 : ")

# driver.find_element(By.검색방법, "검색어")
# 검색 방법은 xpath, css_selector, id 등 여러가지가 존재
# driver.find_element(By.CSS_SELECTOR, "태그와 선택자 조합")
# 검색된 HTML 요소를 리턴
form = driver.find_element(By.CSS_SELECTOR, "textarea#txtSource")  # 번역할 텍스트 입력 블록
# send_keys(값) : HTML요소에 데이터를 전송하는 함수
# HTML 요소에 메소드로 사용, 인자로 전송할 값 전달
form.send_keys(question)

button = driver.find_element(By.CSS_SELECTOR, "button#btnTranslate")  # 번역 버튼
# HTML 요소 클릭
# "Selenium의 HTML요소".click()
button.click()
time.sleep(2)  # 번역 결과 기다림

result = driver.find_element(By.CSS_SELECTOR, "div#txtTarget")  # 번역 결과 텍스트 블록
print(question, "->", result.text)

form.clear()  # 요소의 내용 초기화
time.sleep(3)

driver.close()  # 웹페이지 끄기