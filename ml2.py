import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mat
import numpy as np
import tensorflow as tf
from tensorflow import keras
import seaborn as sns
import os
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings("ignore")
import matplotlib.font_manager as fonm
import prophet
from prophet import Prophet
import matplotlib.dates as mdates
from matplotlib import cm
from tensorflow import keras
from keras.models import Model
from keras.layers import Dense, LSTM
from tensorflow.python.keras import Sequential
import plotly.express as px
import plotly.graph_objects as go
import sqlite3

from mean_db import ml_data

# 한글 변환
mat.rcParams['font.family']='Gulim'

def prediction2():

    st.header('전세 실거래가 예측')
    dbConn=sqlite3.connect("data/mydata.db")
    df_bds1 = pd.read_sql_query('SELECT * FROM budongsan2', dbConn)
    dbConn.close()
    list = df_bds1['SGG_NM'].unique()
    date = df_bds1['CNTRCT_DE'].max()
    
    
    # PATH = 'data/'
    # file_list = os.listdir(PATH + 'ml_data')
    # list = []
    # for i in file_list:
    #     a = i.split('.')[0]
    #     if a !='':
    #         list.append(a)
    # list
    s = st.selectbox('원하는 구를 선택하세요',(list))
    tab1, tab2 = st.tabs(['Tab 1', 'Tab 2'])
    with tab1:
    # 예측모델 1
        check = st.checkbox(f'{s} '"실거래가 예측 수치로 보기 1")
        # data1 = pd.read_csv(PATH + 'ml_data/' + s + '.csv', encoding='cp949', index_col=False)
        data1 = ml_data(s)
        df_train = data1[['CNTRCT_DE', 'RENT_GTN']]
        df_train = df_train.rename(columns={"CNTRCT_DE": "ds", "RENT_GTN": "y"})
        m = Prophet()
        m.fit(df_train)

        future = m.make_future_dataframe(periods=30)
        forecast = m.predict(future)
            # st.write(forecast)

        dates = forecast['ds']
        y_truedates = dates[:len(dates)-30, ]
        y_predates = dates[len(dates)-30:, ]
        if check:
            st.subheader(f'{s} ''실거래가 예측 수치')
            st.write(forecast.loc[forecast['ds'] > date, ['ds','yhat']])
            st.write("👉 ds: 날짜 ,"'yhat: 예측가')
        else:
            st.subheader(f'{s} ''실거래가 예측 그래프')
            fig, ax = plt.subplots()
            ax.plot(y_truedates, forecast.loc[forecast['ds'] <= date, ['trend']],label='past')
            ax.fill_between(x = y_truedates, 
                            y1=forecast.loc[forecast['ds'] <= date, ['yhat_lower']]['yhat_lower'], 
                            y2=forecast.loc[forecast['ds'] <= date, ['yhat_upper']]['yhat_upper'], 
                            color='#70D5F5', alpha=0.2, label='Uncertainty interval'
                            )
            ax.plot(y_predates, forecast.loc[forecast['ds'] > date, ['yhat']],label='prediction')
            ax.fill_between(x = y_predates, 
                            y1=forecast.loc[forecast['ds'] > date, ['yhat_lower']]['yhat_lower'], 
                            y2=forecast.loc[forecast['ds'] > date, ['yhat_upper']]['yhat_upper'], 
                            color='#F55C1A', alpha=0.2, label='Uncertainty interval'
                            )
            ax.legend()
            ax.grid(True, which='major', c='gray', ls='-', lw=1, alpha=0.2)
            ax.set_title('Prophet 모델')
            st.pyplot(fig)
   


    with tab2:
    # 예측 모델 2
        check2 = st.checkbox(f'{s} '"실거래가 예측 수치로 보기 2")
        # data2 = pd.read_csv(PATH + 'ml_data/' + s + '.csv', encoding='cp949', index_col=0)
        data2 = ml_data(s).set_index('CNTRCT_DE')
        y = data2['RENT_GTN'].fillna(method='ffill').values.reshape(- 1, 1)

        # 피처 엔지니어링
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaler = scaler.fit(y)
        y = scaler.transform(y)

        # 학습
        n_forecast = 1 
        n_lookback = 60
        X = []
        Y = []

        for i in range(n_lookback, len(y) - n_forecast + 1):
            X.append(y[i - n_lookback: i])
            Y.append(y[i: i + n_forecast])

        X = np.array(X)
        Y = np.array(Y)

        # train the model
        tf.random.set_seed(0)

        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(X.shape[1], X.shape[2])))
        model.add(LSTM(50, return_sequences=False))
        model.add(Dense(25))
        model.add(Dense(1))

        model.compile(loss='mse', optimizer='adam')
        model.fit(X, Y, epochs=10, batch_size=128, validation_split=0.2, verbose=0)

        # 몇일 예측할지 지정
        n_future = 30
        y_future = []

        x_pred = X[-1:, :, :]  # 마지막으로 관찰된 값
        y_pred = Y[-1]         # 마지막 값

        for i in range(n_future):

            # 과거 데이터 기반
            x_pred = np.append(x_pred[:, 1:, :], y_pred.reshape(1, 1, 1), axis=1)

            # 예측 
            y_pred = model.predict(x_pred)

            # save the forecast
            y_future.append(y_pred.flatten()[0])

        # 미래 데이터
        y_future = np.array(y_future).reshape(-1, 1)
        y_future = scaler.inverse_transform(y_future)

        # 과거 데이터 병합
        df_past = data2[['RENT_GTN']].reset_index()
        df_past.rename(columns={'index': 'Date'}, inplace=True)
        df_past['Date'] = pd.to_datetime(df_past['CNTRCT_DE'])
        df_past['Forecast'] = np.nan

        # 예측 데이터 병합
        df_future = pd.DataFrame(columns=['Date', 'RENT_GTN', 'Forecast'])
        df_future['Date'] = pd.date_range(start=df_past['Date'].iloc[-1] + pd.Timedelta(days=1), periods=n_future)
        df_future['Forecast'] = y_future.flatten()
        df_future['RENT_GTN'] = np.nan

        results = df_past.append(df_future).set_index('Date')
        if check2:
            st.subheader(f'{s} ''실거래가 예측 수치')
            st.write(df_future[['Date','Forecast']])
            st.write("👉 Date: 날짜 ,"'Forecast: 예측가')
            
        else:
            st.subheader(f'{s} ''실거래가 예측 그래프') 
            fig, ax = plt.subplots()
            ax.plot(results['RENT_GTN'], label='past')
            ax.plot(results['Forecast'],label='prediction')
            ax.legend()
            plt.title('LSTM 모델')
            st.pyplot(fig)