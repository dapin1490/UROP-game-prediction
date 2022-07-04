import requests
import json
import pandas as pd

apiLink = "https://api.steampowered.com/IStoreService/GetAppList/v1/?key=372EACF35E336EF628507668AC608CEC&include_games=true&include_dlc=false&include_software=false&include_videos=false&include_hardware=false&last_appid=105450&max_results=1000"
response = requests.get(apiLink)
api_response = json.loads(response.text)  # api로 json 받아서 파싱하기

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

ids = []  # 게임 아이디 리스트
for i in range(len(api_response["response"]["apps"])):
    ids.append(api_response["response"]["apps"][i]["appid"])

# 게임 아이디 리스트로 데이터프레임 만들기
gameIds = pd.DataFrame({"appid": ids})
print(gameIds.info())

# 완성한 데이터프레임을 csv 파일로 저장
gameIds.to_csv("../UROP-game-prediction/prepare data/gameID.csv")

# print(len(watchat_dict))
# print(len(watchat_dict["response"]))
# print(len(watchat_dict["response"]["apps"]))
# print(watchat_dict["response"]["apps"][-1]["appid"])
# print(watchat_dict["response"]["apps"][-1]["name"])