import requests
import bs4
import pandas as pd

kw = input("검색어 입력 : ")

URL = "https://browse.gmarket.co.kr/search?keyword=" + kw  # 크롤링 대상 URL
raw = requests.get(URL)  # 웹페이지 내용(HTML) 요청

html = bs4.BeautifulSoup(raw.text, 'html.parser')  # 텍스트 상태인 코드를 HTML 코드로 변환

# 상품의 큰 틀을 담은 태그 찾기
box = html.find('div', {'class' : 'section__module-wrap', 'module-design-id' : '15'})
# 상품 틀 안의 상품 정보 전부 찾기
items = box.find_all('div', {"class" : 'box__item-container'})
print(len(items))  # 한 페이지당 100개의 상품이 출력되므로 100 출력되어야 정상

product_name = []  # 상품명
prod_price = []  # 가격

for item in items:
    product_name.append(item.find('span', {'class' : 'text__item'}).text.strip())
    prod_price.append(int(item.find('strong', {'class' : 'text__value'}).text.strip().replace(",", "")))

GM_df = pd.DataFrame({
    "name": product_name,
    "price": prod_price
})

print(GM_df.info())
print(GM_df.head())