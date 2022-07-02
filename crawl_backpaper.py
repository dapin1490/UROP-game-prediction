import requests
import json
import pandas as pd
from selenium import webdriver  # 웹페이지를 조작하는 데 필요한 드라이버
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  # 웹드라이버 중 크롬 브라우저용 드라이버
from selenium.webdriver.common.by import By
import time

apiLink = "https://api.steampowered.com/IStoreService/GetAppList/v1/?key=372EACF35E336EF628507668AC608CEC&if_modified_since=3124137600460000000&include_games=true&include_dlc=false&include_software=false&include_videos=false&include_hardware=false"
response = requests.get(apiLink)
api_response = json.loads(response.text)
# &last_appid=0000

'''
응답 구조
"response"
    "apps"
        "appid"
        "name"
        "last_modified"
        "price_change_number"
    "have_more_results"
    "last_appid"
'''

ids = []
for i in range(len(api_response["response"]["apps"])):
    ids.append(api_response["response"]["apps"][i]["appid"])

gameIds = pd.DataFrame({"appid": ids})
print(gameIds.info())

have_more_results = api_response["response"]["have_more_results"]
last_appid = str(api_response["response"]["last_appid"])

while have_more_results:
    more_apiLink = apiLink + "&last_appid=" + last_appid
    response = requests.get(more_apiLink)
    api_response = json.loads(response.text)

    more_ids = []
    for i in range(len(api_response["response"]["apps"])):
        more_ids.append(api_response["response"]["apps"][i]["appid"])
    
    mid = pd.DataFrame({"appid": more_ids})
    gameIds = gameIds.append(mid, ignore_index=True)
    print(gameIds.info())

    try:
        have_more_results = api_response["response"]["have_more_results"]
        last_appid = str(api_response["response"]["last_appid"])
    except KeyError:
        break

    if gameIds["appid"].count() >= 30000:
        break


# print(len(watchat_dict))
# print(len(watchat_dict["response"]))
# print(len(watchat_dict["response"]["apps"]))
# print(watchat_dict["response"]["apps"][-1]["appid"])
# print(watchat_dict["response"]["apps"][-1]["name"])