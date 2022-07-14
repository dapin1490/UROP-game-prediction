import requests
import json
import pandas as pd

apiLink = "https://api.steampowered.com/IStoreService/GetAppList/v1/?key=372EACF35E336EF628507668AC608CEC&include_games=true&include_dlc=false&include_software=false&include_videos=false&include_hardware=false"
more_apiLink = apiLink + "&last_appid=" + str(116120)
response = requests.get(more_apiLink)
api_response = json.loads(response.text)  # api로 json 받아서 파싱하기
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

ids = []  # 게임 아이디 리스트
ids.append(105600)
for i in range(len(api_response["response"]["apps"])):
    ids.append(api_response["response"]["apps"][i]["appid"])

# 게임 아이디 리스트로 데이터프레임 만들기
gameIds = pd.DataFrame({"appid": ids})
print(gameIds.info())

# 더 받을 결과가 있나? / 마지막 게임 아이디(다음 받아올 데이터에 반영)
have_more_results = api_response["response"]["have_more_results"]
last_appid = str(api_response["response"]["last_appid"])

# 더 받을 결과가 있는 한 반복
while have_more_results:
    more_apiLink = apiLink + "&last_appid=" + last_appid  # 마지막 게임 아이디 포함해 링크 생성
    response = requests.get(more_apiLink)
    api_response = json.loads(response.text)  # json 파싱

    more_ids = []  # 게임 아이디
    for i in range(len(api_response["response"]["apps"])):
        more_ids.append(api_response["response"]["apps"][i]["appid"])
    
    # 더 받은 게임 아이디를 데이터프레임으로 만들고 기존 데이터프레임에 병합
    mid = pd.DataFrame({"appid": more_ids})
    gameIds = pd.concat([gameIds, mid], ignore_index=True)
    print(gameIds.info())

    try:  # 여기서 더 받을 데이터가 없다면 반복 종료
        have_more_results = api_response["response"]["have_more_results"]
        last_appid = str(api_response["response"]["last_appid"])
    except KeyError:
        break

    # if gameIds["appid"].count() >= 10000:  # 아니면 게임 아이디가 2만 개 이상 수집되면 종료
    #     break

# 완성한 데이터프레임을 csv 파일로 저장
gameIds.to_csv("../UROP-game-prediction/prepare data/data/gameIDver02.csv")

# print(len(watchat_dict))
# print(len(watchat_dict["response"]))
# print(len(watchat_dict["response"]["apps"]))
# print(watchat_dict["response"]["apps"][-1]["appid"])
# print(watchat_dict["response"]["apps"][-1]["name"])