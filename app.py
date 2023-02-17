# 홈

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import plotly.express as px
import math
from datetime import datetime
from dateutil.relativedelta import relativedelta

st.title('내 방 어디?')

from m0_home.title import run_title
from m1_search.search import run_search
from m2_prediction.predict import run_predict
from m3_chatbot.chatbot import chatrun
from m4_suggestion.suggestions import run_suggestions
from update import update_data


selected3 = option_menu(None, ["🏠Home", "🔎전월세 검색",  "📊전세 예측", "🤖챗봇", '💬건의사항'], 
    # icons=['house', 'cloud-upload', "list-task", 'gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "gray", "font-size": "12.5px"}, 
        "nav-link": {"font-size": "12.5px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#47C83E"},
    }
)

# 홈 탭
if selected3 == "🏠Home":
    run_title()

    
# 전월세 검색 탭
elif selected3 == "🔎전월세 검색":
    run_search()

# 전세 시세 예측 탭 
elif selected3 == "📊전세 예측":
    run_predict()

elif selected3 == "🤖챗봇":
    chatrun()

# 건의사항 탭
elif selected3 == "💬건의사항":
    run_suggestions()

else:
    selected3 == "🏠Home"