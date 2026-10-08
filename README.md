# UROP-game-prediction

학부 연구 프로그램(UROP)에서 진행한 개인 프로젝트 **「딥러닝 기반 게임 흥행 예측」**(2022.05 - 2022.07)의 코드, 데이터, 보고서를 보존한 저장소입니다.

## 프로젝트 개요

- **목표**: 출시 전에 알 수 있는 정보만으로 Steam 게임의 흥행 여부를 예측하는 모델을 만들고, 실제 투자 판단에 활용 가능한 수준인지 확인합니다.
- **데이터**: 2017년 1월부터 2022년 5월까지 Steam에 출시된 유료 게임 828개. Steam Web API와 웹 크롤링으로 가격, 장르, 태그, 지원 언어 수, 개발사·배급사 정보, 리뷰 수, 동시 접속자 수 등을 직접 수집했습니다.
- **실험 설계**: 출시 전 정보만 사용한 **실험군**과, 출시 후 정보(평가 등급, 리뷰 수, 동시 접속자 수 등)까지 포함한 **대조군**으로 나누어 비교했습니다.
- **모델**: DNN(Dropout·Batch Normalization을 포함한 6층 구조), Random Forest, AdaBoost. 모두 10겹 교차검증으로 평가했습니다.
- **보조 모델**: 리뷰 텍스트의 긍정도를 변수로 쓰기 위해 KoNLPy(Mecab) 형태소 분석과 CNN·LSTM·Attention을 결합한 감성 분석 모델을 별도로 만들었습니다. 이 변수는 출시 후 정보이므로 대조군에만 사용했습니다.
- **보고서**: [report/제출본_딥러닝 기반 게임 흥행 예측.pdf](report/%EC%A0%9C%EC%B6%9C%EB%B3%B8_%EB%94%A5%EB%9F%AC%EB%8B%9D%20%EA%B8%B0%EB%B0%98%20%EA%B2%8C%EC%9E%84%20%ED%9D%A5%ED%96%89%20%EC%98%88%EC%B8%A1.pdf)

## 결과

10겹 교차검증 평균 정확도(보고서 기준)는 다음과 같습니다.

| 데이터셋 | DNN | Random Forest | AdaBoost |
| :--- | :---: | :---: | :---: |
| 실험군 (출시 전 정보) | 63.19% | 75.54% | 76.12% |
| 대조군 (출시 후 정보 포함) | 92.59% | 96.38% | 96.07% |

- 실험군에서는 AdaBoost의 평균 정확도가 가장 높았지만 교차검증 회차별 편차가 커서, 편차가 더 작은 Random Forest가 실제 활용에 더 적합하다고 판단했습니다.
- Random Forest 변수 중요도 기준으로 태그, 가격, 지원 언어 수가 흥행 예측에 가장 중요한 변수였습니다.

## 사후 분석 (2026)

포트폴리오를 정리하며 코드와 데이터를 다시 검토해 보니, **대조군 결과에 라벨 누수(target leakage)가 있었습니다.**

- 흥행 라벨(`is_top_seller`)은 Steam 인기 제품 목록에 있는 게임을 1로 표기한 뒤, 나머지 중 **"모든 평가 등급에 'positive'가 포함되고 총 리뷰 수가 500개 이상"인 게임도 1로 다시 표기**하는 방식으로 만들었습니다([`prepare data/[UROP] concat reviews.ipynb`](prepare%20data/%5BUROP%5D%20concat%20reviews.ipynb)).
- 최종 데이터 828개 중 흥행 게임 451개의 약 43%(192개)가 이 규칙으로 흥행 처리되었습니다.
- 그런데 이 규칙에 쓴 '모든 평가 등급'(`all positive`)과 '총 리뷰 수'(`total_review`)가 대조군의 입력 변수에도 포함되어 있었습니다.
- 모델 없이 이 규칙만 적용해도 828개 중 **94.08%**를 맞힐 수 있었습니다. 따라서 대조군의 약 96% 정확도는 출시 후 정보의 예측력이라기보다, 라벨을 만든 규칙을 다시 맞힌 결과에 가깝습니다.
- 실험군에는 이 두 변수가 포함되지 않아, **실험군 결과는 이 문제의 영향을 받지 않습니다.**

지금 다시 진행한다면, 연구 설계 단계에서 수집 데이터와 별개로 흥행 기준을 먼저 구체적으로 정하고, 라벨을 만드는 데 쓴 정보가 모델 입력에 섞이지 않도록 데이터 간 오염을 점검하겠습니다.

## 저장소 구조

노트북과 데이터는 당시 파일명을 그대로 유지했습니다. 노트북은 Google Colab에서 실행되었으며, 코드 안의 파일 경로는 당시 Google Drive 경로입니다.

### 진행 순서

1. **데이터 수집** (`prepare data/*.py`): 게임 ID와 상점 정보, 리뷰를 수집합니다.
2. **데이터 병합 및 라벨링** ([`prepare data/[UROP] concat reviews.ipynb`](prepare%20data/%5BUROP%5D%20concat%20reviews.ipynb)): 인기 제품과 일반 게임 데이터를 합치고 흥행 라벨을 만듭니다.
3. **리뷰 감성 분석** ([`build model/[UROP] is this review positive.ipynb`](build%20model/%5BUROP%5D%20is%20this%20review%20positive.ipynb)): 리뷰 긍정도 변수(`is review positive`)를 만듭니다.
4. **흥행 예측 모델** ([`build model/[UROP] game prediction without under_sampling.ipynb`](build%20model/%5BUROP%5D%20game%20prediction%20without%20under_sampling.ipynb)): 데이터 필터링(828개), 전처리, 실험군/대조군 분리, DNN·Random Forest·AdaBoost 학습 및 평가. **보고서 결과는 이 노트북 기준입니다.**

### `prepare data/` : 데이터 수집 및 병합

- [getGameID_ver01.py](prepare%20data/getGameID_ver01.py), [getGameID_ver02.py](prepare%20data/getGameID_ver02.py) : Steam Web API를 이용해 게임 ID 수집. 01번과 02번의 차이는 API 요청 반복 여부
- [getTopSellerGameID.py](prepare%20data/getTopSellerGameID.py) : Steam 인기 제품 목록에서 게임 ID 수집
- [getTopSellerGameInfo.py](prepare%20data/getTopSellerGameInfo.py) : 인기 제품 게임의 상점 정보 수집
- [getDataFromSteam_01.py](prepare%20data/getDataFromSteam_01.py), [getDataFromSteam_02.py](prepare%20data/getDataFromSteam_02.py) : 게임 ID별 Steam 상점 페이지에서 데이터 수집. 02번 파일이 수집하는 정보가 몇 개 더 많음
- [getDataContinue.py](prepare%20data/getDataContinue.py) : 상점 페이지에서 개발자 라이브 방송이 재생 중이면 페이지 구조가 달라져 수집이 중단되는 문제가 있어, 중단 지점 이후부터 이어서 수집하는 코드
- [getSteamReview.py](prepare%20data/getSteamReview.py) : 게임 리뷰 수집(게임당 1개)
- [`[UROP] concat reviews.ipynb`](prepare%20data/%5BUROP%5D%20concat%20reviews.ipynb) : 인기 제품·일반 게임 데이터 병합 및 흥행 라벨 생성

### `prepare data/data/` : 수집 데이터

- `steam_game_prediction.csv` : **최종 모델 학습에 사용한 데이터**(1,335개). 흥행 예측 노트북에서 출시일·가격·리뷰 수 조건으로 필터링하면 828개가 됩니다.
- `steam_game_prediction_early.csv` : 초기 버전 데이터(474개, 흥행 라벨 없음)
- `topSeller*.csv`, `topSellGameWReview.csv` : 인기 제품 게임 데이터
- `gameID*.csv`, `games*.csv`, `gameWReview*.csv`, `processed_gameWReview.csv` : 일반 게임 수집 데이터 및 중간 산출물
- `steam_trainset.txt` : 리뷰 감성 분석 모델 학습용 레이블 리뷰 데이터

### `build model/` : 모델

- [`[UROP] game prediction without under_sampling.ipynb`](build%20model/%5BUROP%5D%20game%20prediction%20without%20under_sampling.ipynb) : 최종 흥행 예측 모델(보고서 결과 기준)
- [`[UROP] game prediction with under_sampling.ipynb`](build%20model/%5BUROP%5D%20game%20prediction%20with%20under_sampling.ipynb) : 언더샘플링을 적용해 본 실험 버전(보고서 미사용)
- [`[UROP] is this review positive.ipynb`](build%20model/%5BUROP%5D%20is%20this%20review%20positive.ipynb) : 리뷰 감성 분석 모델(최종 버전)
- [is_this_review_positive.ipynb](build%20model/is_this_review_positive.ipynb) : 리뷰 감성 분석 모델 초기 버전

### `report/` : 보고서

- `제출본_딥러닝 기반 게임 흥행 예측.pdf` : 최종 제출 보고서

### `study/` : 크롤링 학습

- 정적·동적 크롤링 연습 코드. 주요 참고 자료: [파이썬 메이트 크롤링 편](https://codemate.kr/project/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EB%A9%94%EC%9D%B4%ED%8A%B8-%ED%81%AC%EB%A1%A4%EB%A7%81-%ED%8E%B8/1-1.-%ED%81%AC%EB%A1%A4%EB%A7%81-%EC%86%8C%EA%B0%9C)
- 논문 스터디 기록: [블로그](https://dapin9104.postype.com/series/952737/%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8)
