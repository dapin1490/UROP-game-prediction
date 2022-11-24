# UROP-game-prediction

## 프로젝트 설명

### 연구 주제

딥러닝 기반 게임 흥행 예측

### 연구 내용

게임에 대한 정보와 소셜 데이터를 분석하여 딥러닝 기반으로 게임의 흥행 여부를 조기에 예측하는 모델을 설계 구현하고 정확성을 측정하며 기존의 기법들과 성능을 비교하고자 한다. 게임 발매 이전에 게임의 판매량 기준으로 게임의 흥행 여부를 예측하여 게임 제작 및 투자에 유용한 정보를 제공하고자 한다.

### 연구 방법

딥러닝 기반으로 게임의 흥행 여부를 예측하기 위하여 게임 장르, 게임 제작사, 게임 발매 시기 등의 게임의 내재적 정보와 온라인 리뷰와 같은 외재적 정보를 함께 고려하여 머신러닝, 딥러닝 모델에 학습시킨다. 널리 알려진 온라인 게임 플랫폼 'STEAM'에서 필요한 내재적 데이터 및 외재적 데이터를 함께 수집할 예정이다. 특히, STEAM에는 고객 리뷰 점수와 전문가 리뷰 점수가 표시되어 있어서 게임의 흥행정도를 예측하는 정량적인 데이터로서 활용 가능하다. DNN, Regression 등의 방법을 이용하고 다양한 변인을 조정하여 성능을 비교한다.

## 파일 설명

### 크롤링 공부

깃허브 : [UROP-game-prediction/study/](https://github.com/dapin1490/UROP-game-prediction/tree/main/study)  
주요 참고 자료 : [https://codemate.kr/project/파이썬-메이트-크롤링-편/1-1.-크롤링-소개](https://codemate.kr/project/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EB%A9%94%EC%9D%B4%ED%8A%B8-%ED%81%AC%EB%A1%A4%EB%A7%81-%ED%8E%B8/1-1.-%ED%81%AC%EB%A1%A4%EB%A7%81-%EC%86%8C%EA%B0%9C)

### 논문 스터디

블로그 : [https://dapin9104.postype.com/series/952737/프로젝트](https://dapin9104.postype.com/series/952737/%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8)  
깃허브에는 업로드하지 않았음

### 데이터 수집

깃허브 : [UROP-game-prediction/prepare data/](https://github.com/dapin1490/UROP-game-prediction/tree/main/prepare%20data)  
  
[getDataFromSteam_01.py](https://github.com/dapin1490/UROP-game-prediction/blob/main/prepare%20data/getDataFromSteam_01.py), [getDataFromSteam_02.py](https://github.com/dapin1490/UROP-game-prediction/blob/main/prepare%20data/getDataFromSteam_02.py) : 게임 ID별 steam 상점 페이지에서 데이터 수집. 02번 파일이 수집하는 정보가 몇 개 더 많음.  
[getDataContinue.py](https://github.com/dapin1490/UROP-game-prediction/blob/main/prepare%20data/getDataContinue.py) : 크롤러가 방문한 상점 페이지에 개발자 생방송이 라이브로 재생되고 있을 경우 특정 정보 수집에 방해가 되어 오류로 수집이 중단됨. 중단지점 이후부터 이어서 수집하는 코드.  
[getGameID_ver01.py](https://github.com/dapin1490/UROP-game-prediction/blob/main/prepare%20data/getGameID_ver01.py), [getGameID_ver02.py](https://github.com/dapin1490/UROP-game-prediction/blob/main/prepare%20data/getGameID_ver02.py) : steam web api를 이용해 게임 ID 수집. 01번과 02번의 차이는 API 요청 반복 여부  
[getSteamReview.py](https://github.com/dapin1490/UROP-game-prediction/blob/main/prepare%20data/getSteamReview.py) : 게임 리뷰 수집. 게임당 1개씩.  
[getTopSellerGameID.py](https://github.com/dapin1490/UROP-game-prediction/blob/main/prepare%20data/getTopSellerGameID.py) : steam 인기 게임 목록으로부터 리스트 내의 게임 ID 수집  
[getTopSellerGameInfo.py](https://github.com/dapin1490/UROP-game-prediction/blob/main/prepare%20data/getTopSellerGameInfo.py) : [getTopSellerGameID.py](https://github.com/dapin1490/UROP-game-prediction/blob/main/prepare%20data/getTopSellerGameID.py)에서 ID를 수집한 게임들의 정보 수집  

### 모델 설계 및 실행

[build model](https://github.com/dapin1490/UROP-game-prediction/tree/main/build%20model)

https://github.com/dapin1490/UROP-game-prediction/blob/main/prepare%20data/
