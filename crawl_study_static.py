# reference https://codemate.kr/project/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EB%A9%94%EC%9D%B4%ED%8A%B8-%ED%81%AC%EB%A1%A4%EB%A7%81-%ED%8E%B8/1-1.-%ED%81%AC%EB%A1%A4%EB%A7%81-%EC%86%8C%EA%B0%9C

import requests
import bs4

URL = "https://dhlottery.co.kr/gameResult.do?method=byWin"
raw = requests.get(URL)
# print(raw.content, end="\n\n")
print(raw)  # HTTP requests code reference : https://ko.wikipedia.org/wiki/HTTP_%EC%83%81%ED%83%9C_%EC%BD%94%EB%93%9C

html = bs4.BeautifulSoup(raw.content, 'html.parser', from_encoding='euc-kr')

# target : <div class="nums">
targ = html.find('div', {'class' : 'nums'})
balls = targ.find_all("span", {'class' : 'ball_645'})

print("< 최근 로또 당첨 번호 >")
for ball in balls[:-1]:
    print("당첨번호 : ", ball.text)

print("보너스 번호 : ", balls[-1].text)