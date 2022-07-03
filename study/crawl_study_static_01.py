# reference https://codemate.kr/project/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EB%A9%94%EC%9D%B4%ED%8A%B8-%ED%81%AC%EB%A1%A4%EB%A7%81-%ED%8E%B8/1-1.-%ED%81%AC%EB%A1%A4%EB%A7%81-%EC%86%8C%EA%B0%9C

import requests
import bs4

URL = "https://dhlottery.co.kr/gameResult.do?method=byWin"  # 크롤링 대상 URL
raw = requests.get(URL)  # 웹페이지의 내용(HTML) 요청
# print(raw.content, end="\n\n")
# 요청 성공 여부 확인 : 2로 시작하는 코드가 나오면 성공
print(raw)  # HTTP requests code reference : https://ko.wikipedia.org/wiki/HTTP_%EC%83%81%ED%83%9C_%EC%BD%94%EB%93%9C

# 문자열 타입인 raw의 코드를 HTML로 변환
# bs4.BeautifulSoup("HTML 데이터", "데이터 타입")
html = bs4.BeautifulSoup(raw.content, 'html.parser')

# target : <div class="nums">
targ = html.find('div', {'class' : 'nums'})  # first-fit 탐색
balls = targ.find_all("span", {'class' : 'ball_645'})  # fit하는 모든 값 탐색

print("< 최근 로또 당첨 번호 >")
for ball in balls[:-1]:
    print("당첨번호 : ", ball.text)  # 텍스트만 추출하여 출력

print("보너스 번호 : ", balls[-1].text)