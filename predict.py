import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib
matplotlib.use('Agg')
import plotly.graph_objects as go
import geopandas as gp

from datetime import datetime
from dateutil.relativedelta import relativedelta
from stqdm import stqdm
from time import sleep
import warnings
warnings.filterwarnings("ignore")
from stqdm_model import stqdm_model
from ml2 import prediction2
from update import update_data
from mean_db import dong_j_d_mean, gu_j_d_mean, gu_j_m_mean, gu_w_d_mean, gu_w_m_mean

def run_predict():
    st.markdown("""
    *👉 왼쪽 메뉴를 선택하세요*
    """)
    
    # df = pd.read_csv('data/bds_data.csv', encoding='cp949')
    df = update_data()
    df = pd.DataFrame(df)
    df_copy = df.copy()
    # data = pd.read_csv('data/bds_data.csv', encoding='cp949')
    data = df
    st.write(df)
    
    sub_menu = ['전월세 월평균 그래프', '전월세 실거래수 지역 순위', '날짜별 거래', '전세 예측', '전월세 전환율/대출이자 계산기']
    sub_choice = st.sidebar.selectbox("메뉴", sub_menu)

    now = datetime.now()
    before_day = now - relativedelta(days=1)
    before_month = before_day - relativedelta(months=1)
    before_day = before_day.strftime("%Y-%m-%d")
    before_month = before_month.strftime("%Y-%m-%d")

    if sub_choice == '전월세 월평균 그래프':
        st.subheader("전월세 월평균 그래프")
        # j_m_mean = pd.read_csv('data/gu_j_m_mean.csv', encoding='cp949')
        j_m_mean = gu_j_m_mean(df)
        # w_m_mean = pd.read_csv('data/gu_w_m_mean.csv', encoding='cp949')
        w_m_mean = gu_w_m_mean(df)
        gu = np.array(j_m_mean['SGG_NM'].unique())
        gu = st.multiselect('구를 선택하세요.', gu, default=['서초구', '강남구', '용산구'])
        t1, t2 = st.tabs(['전세 월평균 그래프', '월세 월평균 그래프'])
        with t1:
            c1 = st.checkbox('전세 월평균 그래프', True)
            fig = go.Figure()
            if c1:
                fig = px.scatter(width=700)
                for j in gu:
                    df = j_m_mean[j_m_mean['SGG_NM']==j]
                    fig.add_scatter(x=df['YM'], y=df['RENT_GTN'], name=j)
                fig.update_layout(xaxis_title='날짜', yaxis_title='보증금(k=천만원)')
                st.plotly_chart(fig)
            else:
                a = 0
                for i in gu:
                    jm = pd.DataFrame(j_m_mean[j_m_mean['SGG_NM']==i])
                    if a == 0:
                        js = jm
                        a += 1
                    else:
                        js = pd.concat([js , jm])
                st.write(js)

        with t2:
            c1 = st.checkbox('보증금 월평균 그래프', True)
            
            fig = go.Figure()
            if c1:
                fig = px.scatter(width=700, height=350)
                for j in gu:
                    df = w_m_mean[w_m_mean['SGG_NM']==j]
                    fig.add_scatter(x=df['YM'], y=df['RENT_GTN'], name=j)
                fig.update_layout(xaxis_title='날짜', yaxis_title='보증금(k=천만원)')
                st.plotly_chart(fig)
            else:
                a = 0
                for i in gu:
                    wm = pd.DataFrame(w_m_mean[w_m_mean['SGG_NM']==i])
                    wm = wm.drop(columns=['RENT_FEE'],axis=0)
                    if a == 0:
                        ws = wm
                        a += 1
                    else:
                        ws = pd.concat([ws , wm])
                st.write(ws)
                
            c2 = st.checkbox('월세 월평균 그래프', True)
            if c2:
                fig = px.scatter(width=700, height=350)
                for j in gu:
                    df = w_m_mean[w_m_mean['SGG_NM']==j]
                    fig.add_scatter(x=df['YM'], y=df['RENT_FEE'], name=j)
                fig.update_layout(xaxis_title='날짜', yaxis_title='보증금(k=천만원)')
                st.plotly_chart(fig)
            else:
                a = 0
                for i in gu:
                    wm = pd.DataFrame(w_m_mean[w_m_mean['SGG_NM']==i])
                    wm = wm.drop(columns=['RENT_GTN'],axis=0)
                    if a == 0:
                        ws = wm
                        a += 1
                    else:
                        ws = pd.concat([ws , wm])
                st.write(ws)
    
    elif sub_choice == '전월세 실거래수 지역 순위':
        t1, t2 = st.tabs(['월세', '전세'])
        with t1:
            st.subheader("""
            📗 현재 월세 실거래수 TOP 10
            """)

            # 월세인 데이터 추출
            data_m = data[(data['RENT_GBN'] == '월세') & (data['CNTRCT_DE']>=f'{before_month}')]
            # 구, 동 합치기
            cols = ['SGG_NM', 'BJDONG_NM']
            data_m['주소'] = data_m[cols].apply(lambda row:' '.join(row.values.astype(str)),axis=1)
            data_addr = data_m['주소'].value_counts().rename_axis('주소').reset_index(name='거래 수')
            #인덱스 재지정
            data_addr = data_addr.reset_index(drop=True)
            data_addr.index = data_addr.index+1
            # 그래프
            c1 = st.checkbox('최근 한달 월세 실거래 수 지역 순위 그래프', True)
            st.write('#### 기간 : ' + f'{before_month}' + ' ~ ' + f'{before_day}')
            fig = go.Figure()
            if c1:
                fig = px.bar(x=data_addr.head(10)['주소'], y=data_addr.head(10)['거래 수'], width=700,
                            color=data_addr.head(10)['주소'])
                fig.update_layout(xaxis_title='지역 동', yaxis_title='거래 수')
                st.plotly_chart(fig)
            else:
                # 데이터
                st.write(data_addr.head(10))
        # 전세 실거래 수 지역 순위(월세와 같은 방식)
        with t2:
            st.subheader("""
            📘 현재 전세 실거래수 TOP10
            """)
            
            data_m = data[(data['RENT_GBN'] == '전세') & (data['CNTRCT_DE']>=f'{before_month}')]
            cols = ['SGG_NM', 'BJDONG_NM']
            data_m['주소'] = data_m[cols].apply(lambda row:' '.join(row.values.astype(str)),axis=1)
            data_addr = data_m['주소'].value_counts().rename_axis('주소').reset_index(name='거래 수')
            data_addr = data_addr.reset_index(drop=True)
            data_addr.index = data_addr.index+1
            # 그래프
            c1 = st.checkbox('최근 한달 전세 실거래 수 지역 순위 그래프', True)
            st.write('#### 기간 : ' + f'{before_month}' + ' ~ ' + f'{before_day}')
            fig = go.Figure()
            if c1:
                fig = px.bar(x=data_addr.head(10)['주소'], y=data_addr.head(10)['거래 수'], width=700,
                            color=data_addr.head(10)['주소'])
                fig.update_layout(xaxis_title='지역 동', yaxis_title='거래 수')
                st.plotly_chart(fig)
            else:
                # 데이터
                st.write(data_addr.head(10))
    elif sub_choice == '날짜별 거래':
        st.subheader("날짜별 거래")
        date1 = st.date_input("날짜선택")
        
        dgg = gp.read_file("data/ef.geojson")
        # dff =  pd.read_csv("data/dong_j_d_mean.csv",encoding='euc-kr')
        dff = dong_j_d_mean(df)
        date2 = st.selectbox("동 선택", dgg['adm_nm'].unique())
        map_dong = dgg[dgg['adm_nm'] == f'{date2}']
        map_si = dff[dff['CNTRCT_DE'] == f'{date1}']
        merged = map_dong.set_index('adm_nm').join(map_si.set_index('BJDONG_NM'))
        fig = px.choropleth_mapbox(merged, geojson=merged.geometry, locations=merged.index, color="RENT_GTN", mapbox_style="carto-positron", zoom=9.8,
        center = {"lat": 37.575651, "lon": 126.97689}, opacity=0.6)
        fig.update_geos(fitbounds="locations", visible=True)
        if  merged["RENT_GTN"].values > 0:
            st.plotly_chart(fig)
        else:
            st.markdown('# 금일 거래는 없습니다.')
            st.plotly_chart(fig)
    elif sub_choice == '전세 예측':

        st.subheader("전세 예측")
        prediction2()
        
    elif sub_choice == '전월세 전환율/대출이자 계산기':
        # 전월세 전환율 계산기 / 이자 계산
        st.subheader('전월세 전환율 계산기')
        st.markdown('***')
        st.write("#### 전세 -> 월세")
        c1, c2, c3 = st.columns([1,1,1])

        p1 = c1.empty()
        p2 = c2.empty()
        p3 = c3.empty()
        with p1.container():
            n1 = st.number_input("전월세 전환율 (%)", step=0.1)
        with p2.container():
            n2 = st.number_input("월세 보증금 (만원)", step=0.1)
        with p3.container():
            n3 = st.number_input("전세 보증금 (만원)", step=0.1)
        nRe = ((n3-n2)*(n1/100))/12
        if nRe <= 0:
            nRe = 0
        # n4 = st.number_input("월세 (만원)", step=0.1, value=float(nRe))
        st.write('월세(만원)')
        st.success(str(f'{nRe:.2f}') + '만원')
        p1 = st.empty()
        p2 = st.empty()
        p3 = st.empty()

        st.markdown('***')
        st.write("#### 월세 -> 전세")
        c4, c5, c6 = st.columns([1,1,1])
        p4 = c4.empty()
        p5 = c5.empty()
        p6 = c6.empty()
        with p4.container():
            u1 = st.number_input("전월세 전환율 (%) ", step=0.1)
        with p5.container():
            u2 = st.number_input("월세 보증금 (만원) ", step=0.1)
        with p6.container():
            u3 = st.number_input("월세 (만원) ", step=0.1)

        if u1 == 0:
            uRe = 0
        else:
            uRe = ((u3*12)/(u1/100)) + u2

        # u4 = st.number_input("전세 보증금 (만원) ", step=0.1, value=float(uRe))
        st.write('전세 보증금 (만원)')
        st.success(str(f'{uRe:.2f}') + '만원')
        p4 = st.empty()
        p5 = st.empty()
        p6 = st.empty()

        st.markdown('***')
        st.write("#### 대출 이자 계산")
        e = st.selectbox('상환 방법', ['원리금균등상환', '원금균등상환', '원금만기일시상환'])
        c7, c8, c9 = st.columns([1,1,1])
        p7 = c7.empty()
        p8 = c8.empty()
        p9 = c9.empty()
        
        with p7:
            e1 = st.number_input('대출 금액(원)', step=1)
        with p8:
            e2 = st.number_input('대출 금리(연 %)', step=0.1)
        with p9:
            e3 = st.number_input('대출 기간(개월)', step=1)
        if e == '원리금균등상환':
            R = e2/1200
            N = (1+R)**e3
            if (N-1) <= 0:
                eRe1 = 0
                eRe2 = 0
            else:
                eRe1 = (e1*R*N)/(N-1)
                eRe2 = 0
        elif e == '원금균등상환':
            eRe1 = e1*(e2/100)*((e3+1)/24)
            eRe2 = eRe1/e3
        else:
            eRe1 = e1*(e2/1200)*e3
            eRe2 = eRe1/e3
        eRe1 = float(eRe1)
        if e == '원리금균등상환':
            # e5 = st.number_input('매월 상환금 (원금 + 이자) (원)', step=0.1, value=float(eRe1))
            st.write('매월 상환금 (원금 + 이자)')
            st.success(str(f'{eRe1:.0f}') + '원')
        else:
            ce1, ce2 = st.columns([1,1])
            pe1 = ce1.empty()
            pe2 = ce2.empty()
            with pe1:
                # e5 = st.number_input('총 이자 금액', step=0.1, value=float(eRe1))
                # st.write('총 이자 금액')
                st.success('총 이자 금액　　　　　　　　　' + str(f'{eRe1:.0f}') + '원')
            with pe2:
                # e6 = st.number_input('월별 이자 금액', step=0.1, value=float(eRe2))
                # st.write('월별 이자 금액')
                st.success('월별 이자 금액　　　　　　　　　' + str(f'{eRe2:.0f}') + '원')
            p7 = st.empty()
            p8 = st.empty()
            p9 = st.empty()

        st.markdown('***')
        st.write("#### 전환율 계산")
        c11, c12, c13 = st.columns([1,1,1])
        p11 = c11.empty()
        p12 = c12.empty()
        p13 = c13.empty()
        with p11.container():
            m1 = st.number_input("전세 보증금 (만원)  ", step=0.1)
        with p12.container():
            m2 = st.number_input("월세 보증금 (만원)  ", step=0.1)
        with p13.container():
            m3 = st.number_input("월세 (만원)  ", step=0.1)
        
        if (m1-m2) == 0:
            mRe = 0
        else:
            mRe = ((m3*12)/(m1-m2))*100
        # m4 = st.number_input("전월세 전환율 (%)  ", step=0.1, value=float(mRe))
        st.write('전월세 전환율 (%)')
        st.success(str(f'{mRe:.2f}') + '%')
        p11 = st.empty()
        p12 = st.empty()
        p13 = st.empty()