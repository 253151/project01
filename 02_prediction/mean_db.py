import pandas as pd
import numpy as np
import sqlite3
import streamlit as st

# 구별 전세 일 평균
def gu_j_d_mean(df_bds):
    df_bds['RENT_GTN'] = df_bds['RENT_GTN'].astype(int)
    df = df_bds.drop(df_bds[df_bds['RENT_GBN']=='월세'].index, axis=0)
    df2 = df.groupby(['SGG_NM','CNTRCT_DE'])['RENT_GTN'].mean().reset_index()
    return df2

# 구별 전세 월 평균
def gu_j_m_mean(df_bds):
    df_bds['RENT_GTN'] = df_bds['RENT_GTN'].astype(int)
    df = df_bds.drop(df_bds[df_bds['RENT_GBN']=='월세'].index, axis=0)
    df['YM'] = df['CNTRCT_DE'].str.slice(start=0,stop=7)
    df2 = df.groupby(['SGG_NM', 'YM'])['RENT_GTN'].mean().reset_index()
    return df2

# 구별 월세 일 평균
def gu_w_d_mean(df_bds):
    df_bds['RENT_GTN'] = df_bds['RENT_GTN'].astype(int)
    df = df_bds.drop(df_bds[df_bds['RENT_GBN']=='전세'].index, axis=0)
    df2 = df.groupby(['SGG_NM','CNTRCT_DE'])['RENT_GTN'].mean().reset_index()
    return df2

# 구별 월세 월 평균
def gu_w_m_mean(df_bds):
    df_bds['RENT_GTN'] = df_bds['RENT_GTN'].astype(int)
    df_bds['RENT_FEE'] = df_bds['RENT_FEE'].astype(int)
    df = df_bds.drop(df_bds[df_bds['RENT_GBN']=='전세'].index, axis=0)
    df['YM'] = df['CNTRCT_DE'].str.slice(start=0,stop=7)
    df2 = df.groupby(['SGG_NM', 'YM'])['RENT_GTN', 'RENT_FEE'].mean().reset_index()
    return df2

# 동별 전세 일 평균
def dong_j_d_mean(df_bds):
    df_bds['RENT_GTN'] = df_bds['RENT_GTN'].astype(int)
    df = df_bds.drop(df_bds[df_bds['RENT_GBN']=='월세'].index, axis=0)
    df2 = df.groupby(['BJDONG_NM','CNTRCT_DE'])['RENT_GTN'].mean().reset_index()
    return df2

# ml2.py 구별 data
def ml_data(gu):
    dbConn=sqlite3.connect("data/mydata.db")
    df_bds1 = pd.read_sql_query('SELECT * FROM budongsan2', dbConn)
    # cs=dbConn.cursor()
    # cs.execute('SELECT * FROM budongsan2')
    # df_bds = cs.fetchall()
    dbConn.close()

    df_bds2 = pd.DataFrame(df_bds1)
    df = pd.DataFrame(gu_j_d_mean(df_bds2))
    df = df[df['SGG_NM']==gu]
    df2 = df.drop(columns=['SGG_NM'])
    return df2