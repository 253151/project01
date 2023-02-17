# 홈

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import plotly.express as px
import math
from datetime import datetime
from dateutil.relativedelta import relativedelta



def run_title(data):
    """
    홈페이지입니다.
    SQLiteDB(mydata.db)에서 불러온 서울시 전월세가 실거래 데이터(budongsan2(update.py 참고))를 리턴하는 함수입니다
    :param: 
    :return: 가공한 data를 리턴합니다.
    """
    data = update_data()
    # data = pd.read_csv('data/bds_data.csv', encoding='cp949')
    data2 = data.copy()
    po = data2['SGG_NM'] == '영등포구'
    tel = data2['HOUSE_GBN_NM'] == '아파트'
    # st.write(data2[po & tel]['BOBN'].count())

    now = datetime.now()
    before_day = now - relativedelta(days=1)
    before_month = before_day - relativedelta(months=1)
    before_day = before_day.strftime("%Y-%m-%d")
    before_month = before_month.strftime("%Y-%m-%d")

    with st.sidebar:
        st.markdown('# 　　　　　목차')
        st.markdown('## HOME\n ### 전월세 검색\n ### 전세 예측\n - 전월세 평균 그래프\n - 전월세 실거래수 지역 순위\n - 날짜별 거래\n - 전세 예측\n - 전월세 전환율 / 대출이자 계산기 \n### ChatBot\n ### 건의 사항')


    # 실거래 현황
    st.subheader('최근 한달 실거래 현황 (최신순)')
    st.write("기간 : " + f'{before_month}' + " ~ " +f'{before_day}' + " (계약일 기준)")
    data = data[data['CNTRCT_DE']>=f'{before_month}']
    
    # FLR_NO 값에 "층"을 더해줌
    data['FLR_NO'] = data['FLR_NO'].astype(str) + '층' 
    # 본번과 부번을 합침
    cols = ['BOBN', 'BUBN'] 
    # 번지 = 부번이 0이 아니면 cols 사이에 "-" 를 더해줌 (본번-부번), 0일시에는 본번만 나타냄
    data['번지'] = data[cols].apply(lambda row: '-'.join(row.values.astype(str)) 
                                            if row['BUBN'] != 0 
                                            else row['BOBN'], axis=1) 
    # 'BLDG_NM' 컬럼에서 아파트, 오피스텔이 있으면 없애줌
    data['BLDG_NM'] = data['BLDG_NM'].str.replace('아파트', '')
    data['BLDG_NM'] = data['BLDG_NM'].str.replace('오피스텔', '') 
    # 전체 주소 변환 결과를 더함          
    cols1 = ['SGG_NM', 'BJDONG_NM', '번지', 'BLDG_NM', 'HOUSE_GBN_NM', 'FLR_NO'] 
    # 주소란의 최종 출력값!!
    data['주소'] = data[cols1].apply(lambda row:' '.join(row.values.astype(str)),axis=1) 
    # 원본데이터를 Drop
    data = data.drop(['SGG_CD', 'BJDONG_CD', 'SGG_NM', 'BJDONG_NM', 'BOBN', 'BUBN', 'FLR_NO', 'BLDG_NM', '번지', 'HOUSE_GBN_NM'], axis=1)
    # 임대면적을 m² → 평 단위로 변환
    data['RENT_AREA'] = data['RENT_AREA'].apply(lambda x: math.trunc(x / 3.3058)) 
    # data 컬럼명
    data.columns = ['계약일', '전월세 구분', '임대면적(평)', '보증금(만원)', '임대료(만원)', '건축년도', '주소']
    # 출력순서
    data = data[['계약일', '주소', '보증금(만원)', '임대료(만원)', '임대면적(평)', '건축년도', '전월세 구분']]
    data = data.reset_index(drop=True)
    data.index = data.index+1
    st.write(data)