# reference https://codemate.kr/project/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EB%A9%94%EC%9D%B4%ED%8A%B8-%ED%81%AC%EB%A1%A4%EB%A7%81-%ED%8E%B8/1-1.-%ED%81%AC%EB%A1%A4%EB%A7%81-%EC%86%8C%EA%B0%9C

import requests
import bs4

req = requests.get("https://comic.naver.com/webtoon/weekday")
# print(req.text, end="\n\n")

html = bs4.BeautifulSoup(req.text, 'html.parser')
# print(html, end="\n\n")

columns = html.find_all('div', {'class':'col_inner'})

for column in columns:
    day = column.find('h4').text
    webtoons = column.find_all('a', {'class' : 'title'})[:5]
    print(day)
    for index in range(len(webtoons)):
        title = webtoons[index].text
        print(f"{index+1}. {title}")
    print()