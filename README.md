# *📕 PROJECT01. 내 방, 어디?*

 - **사용언어** : Python 3.9.13
 - **사용툴** : VS Code 1.74.1, Google Colab
 - **사용 라이브러리** : 
 > _numpy_ 1.24.0, _pandas_ 1.5.3, _matplotlib_ 3.6.3, _streamlit_ 1.18.0, _plotly_ 5.13.0, 
 > *tensorflow* 2.9.0, *streamlit_option_menu* 0.3.2, _geopandas_ 0.12.2, _joblib_ 1.2.0, 
 > *scikit-learn* 1.2.1, *pandas-gbq* 0.17.9, *pydeck* 0.8.0, *prophet* 1.1.2, *seaborn* 0.12.2, 
 > *openai* 0.26.5, *streamlit_chat* 0.0.2.1, *requests* 2.28.2
 - **프로젝트 내용**
    - 서울공공API를 이용하여 매일 업데이트 되는 전월세 실거래 현황 데이터
    - 그래프를 통한 전월세 실거래가 월별/날짜별 정보 제공, 전월세 시세 정보 제공
    - 구별 부동산 전세 시세 예측
    - 전월세 전환율 및 전세 대출 이자 계산기
    - 챗봇을 통한 구+ 날짜별 실거래가 검색
    - 건의사항

 - **프로젝트 인원** : 총7명
    - 개발(4명)
    - 데이터(3명)
 - **기간** : 2023.01.30 ~ 02.10 (약 2주)

 - 데이터👉  [서울시 부동산 전월세가 정보](https://data.seoul.go.kr/dataList/OA-21276/S/1/datasetView.do)
 - 내방어디👉 [클릭](https://whereismyroom.streamlit.app/)


## 소스코드
- 자세한 설명은 각각의 파일 주석 참고
- **Index**
    ```Markdown
    1. 00_home: 홈 탭 
    2. 01_search: 전월세 검색
    3. 02_prediction: 전세예측
    4. 03_chatbot: 챗봇
    5. 04_suggestion: 건의사항
    6. data: 데이터 모음
    7. app.py: 메뉴 바 및 실행 함수
    8. git.bat: github 업로드 배치 파일
    9. requirements.txt: 사용 라이브러리
    10. sql.py: db생성
    11. batchFile.bat: API 접속 및 업데이트
    12. update.py: run_update 함수
    ```


## Daily Update

### ▷ 01.30
 - 시나리오 구상


### ▷ 01.31
#### 개발팀
-  오늘 한 것
    - streamlit 배포
    - 전체적인 STORY 구상
    - 기본적인 UI 구현
-  오늘 못한 것
    - 추천기능try: 거래매물이 많은 지역
    (or 면적당 가격이 싼 곳)
    - 전, 월세 검색 페이지 구현
    - 건의사항 페이지 구현
-  내일 할 것
    - 전/월세 검색기능
    - 전/월세 비교
    - 결과물 동기화

#### 데이터팀
-  오늘 한것
    - DATA 전처리 진행(ING)
    - 결측치 제거, 불필요한 데이터 제거
    - 시나리오 작성
-  하지 못한것(내일 할것)
    - DATA 전처리
    - 월 평균 예측치 분석
    - 시나리오 재작성
    - 시각화, 예측모델


### ▷ 02.01
#### 개발팀
-  오늘 한 것
    - home 페이지
        + 기본적인 layer 구상
        + 거래횟수가 많은 지역 순으로 데이터 정렬
    - 전/월세 페이지
        + sidebar에서 조건에 맞는 검색 기능
        + 보증금, 월세, 면적의 최소, 최댓값을 지정해주는 슬라이더
        + 버튼 누를 시 선택된 값에 해당하는 검색 결과
        + 면적 제곱미터를 평수로 변환하는 람다식
        + 필요한 칼럼을 조인하여 데이터 가공
        + 특정 칼럼에서 특정문자 삭제
    - 건의사항 페이지
        + 게시판 UI 및 기능 구현
        + sqlite 데이터베이스 연동
    - 전체
        + 코드 동기화
- 오늘 못한 것
    - home 페이지
        + 정렬한 데이터 추출
    - 전월세 페이지
        + 전세와 월세를 동시에 보여주는 기능
        + 보증금 월세 범위가 예상보다 컸음
    - 건의사항 페이지
        + 게시글 수정&삭제 기능
-  내일 할 것
    - 데이터 추가 핸들링
    - home 페이지 디자인 마무리
    - 전세예측 페이지 구현
    - 게시글 수정 & 삭제 기능
    - 건의사항 내용 칸 늘리기

#### 데이터팀
-  오늘 한 것
    - 데이터 전처리 정리
    - 최적시각화 그래프 서칭
    - 프로젝트시나리오 재작성
    - streamlit  사용하여 구, 동선택 가능한 multislectbox 구현
    - 구, 동별 데이터 시각화코드 작성
-  오늘 못한 것
    - 데이터전처리(일일평균)
    - 그래프 최적화
-  내일 할 것
    - 구, 동별 일일 평균 시각화 코드 작성
    - 막대 및 지도 시각화
    - 시나리오 보충
 

### ▷ 02.02
#### 개발팀
-  오늘 한 것
    - homepage UI 디자인변경
    - homepage dataframe구성 변경
    - 월/전세 전체 검색기능
    - 월세, 보증금, 면적검색할 때 최소, 최댓값 입력 기능
    - 건의사항 목록 간격 수정
    - 건의사항 처리상태 변경 기능
    - 건의사항 제목, 사용자명 검색 기능
-  오늘 못한 것
    - 지역에 맞춘 keyword 알고리즘
    - 건의사항 게시글 조회, 수정, 삭제 기능
-  내일 할 것
    - homepage keyword 알고리즘 구현
    - 건의사항 검색 UI 수정
    - 건의사항 내용 검색 기능(디버깅)
    - 건의사항 검색 시 목록 수정
    - 건의사항 목록 간격

#### 데이터팀
-  오늘 한 것
    - 데이터 전처리 정리
    - 최적시각화그래프서칭
    - 지도그래프시각화코드작성(미완)
    - 프로젝트 시나리오 재작성
    - streamlit 사용하여 구, 동 선택가능한 multislectbox 구현
    - 구, 동별 데이터 시각화코드작성
-  오늘 못한 것
    - 데이터전처리(일일평균)
    - 지도 그래프 시각화 코드 작성(미완)
    - 그래프 최적화
-  내일 할 것
    - 구, 동별일일평균 시각화 코드 작성
    - 막대 및 지도 시각화
    - 시나리오 보충


### ▷ 02.03
#### 개발팀
-  오늘 한 것
    - 검색 페이지 슬라이더 기능 조정
        + 슬라이더와 텍스트박스값 연동
    - 건의사항
        + 게시글 조회 기능
        + UI 변경
        + 관리자 메뉴 기능 추가
    -  오늘 못한 것
    - csv데이터값 결함 수정
        + 월/전세 구분 오류 확인
    - 건의사항 목록 간격 지정
-  내일 할 것
    - csv데이터값 결함 수정
    - 건의사항 관리자 메뉴 숨기기

#### 데이터팀
-  오늘 한 것
    - json 파일 변경
    - csv파일과 json파일 병합
    - 지도 시각화 구현
    - 실거래가 머신러닝 코드 분석
    - 월세 실거래수 지역 순위 막대그래프 구현
    - 전세 실거래 수 지역 순위 막대그래프 구현
    - 전세 및 월세(보증금) 월 평균 라인그래프 구현
    - 실거래가 데이터 전처리 진행
-  오늘 못한 것
    - 실거래가 머신러닝 코드 구현
    - 전세 및 월세 실거래가 데이터 전처리
    - 전세 및 월세 실거래가 계산 레이아웃 구현
-  다음주 할 것
    - 실거래가 머신러닝 코드 구현
    - 전세 및 월세 실거래가 데이터 전처리
    - 전세 및 월세 실거래가 계산 레이아웃 구현
    - 지도 시각화 수정


### ▷ 02.06
#### 개발팀
-  오늘 한 것
    - BigQuery를 통한 data cloud 구현 시도 
-  오늘 못한 것
    - 실시간 데이터 수집(api로 받기)
-  내일 할 것
    - 실시간 데이터 수집
    - 홈페이지 기능 재배치

#### 데이터팀
-  오늘 한 것
    - json 파일 geojson 으로 변경
    - csv 파일과 json 파일 병합
    - 지도 시각화 구현(완료)
    - 실거래가 머신러닝 코드 분석(진행중)
    - 실거래가 데이터 전처리 진행(완료)
- 오늘 못한 것
    - 실거래가 머신러닝 코드 구현(진행중)
    - 전세 및 월세 실거래가 계산 레이아웃 구현(진행중)
- 내일 할 것
    - 실거래가 머신러닝 코드 구현

### ▷ 02.07
#### 개발팀
-  오늘 한 것
    - 홈페이지 재배치
    - 검색 slider에 scale 추가
    - API data를 DB에 연결
-  오늘 못한 것
    - 실시간 데이터 수집
        + batch process 구현
-  내일 할 것
    - batch process 구현

#### 데이터팀
-  오늘 한 것
    - 실거래가 머신러닝 코드 구현1(완료)
    - 실거래가 머신러닝 코드 분석(완료)
    - 전세 및 월세 실거래가 계산 레이아웃 구현(진행중)
-  오늘 못한 것
    - 실거래가 머신러닝 코드 구현2(진행중)
    - 전세 및 월세 실거래가 계산 레이아웃 구현(진행중)
-  내일 할 것
    - 실거래가 머신러닝 코드 구현2
    - 전세 및 월세 실거래가 계산 코드 작성


### ▷ 02.08
#### 개발팀
-  오늘 한 것
    - 건의사항 UI 수정
    - 건의사항 수정/삭제, 자주 묻는 질문 탭 추가
    - batch process 구현
-  오늘 못한 것
    - 전월세 검색 페이지 버그 수정
-  내일 할 것
    - 전월세 검색 페이지에 조회버튼 버그 수정
    - 배치파일을 이용해 update되는지 확인

#### 데이터팀
-  오늘 한 것
    - LSTM 예측 모델 보완
    - prophet 예측 모델 완성
    - 그래프 레이아웃 시각화 수정( 구 선택 추가 )
    - ChatBot 데이터 연동
    - 전월세 전환 계산 1 구현 ( 전세- -> 월세 )
-  오늘 못 한 것
    - 머신러닝 시각화 레이아웃 수정
    - 전월세 전환 계산 2,3 구현( 월세--> 전세, 전환율 계산)
-  내일 할 것
    - ChatBot 데이터 수정
    - 머신러닝 시각화 레이아웃 수정
    - 전월세 전환 계산 2,3 구현( 월세--> 전세, 전환율 계산)


### ▷ 02.09-10
- 프로젝트 코드 취합 및 배포