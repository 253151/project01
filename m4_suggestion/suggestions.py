# 건의사항 탭
import streamlit as st
import sqlite3
import time
import pandas as pd
from PIL import Image


conn = sqlite3.connect('data/suggestion.db', check_same_thread=False)
cur = conn.cursor()

# 테이블 생성
def create_tb():
    cur.execute('CREATE TABLE IF NOT EXISTS suggestion(author CHAR, pword CHAR, email VARCHAR, title TEXT, comment TEXT, date TEXT, status TEXT)' )
    conn.commit()

# 게시글 db 입력
def add_data(author, pword, email, title, comment, date, status):
    params = (author, pword, email, title, comment, str(date), status)
    cur.execute("INSERT INTO suggestion(author, pword, email, title, comment, date, status) VALUES (?,?,?,?,?,?,?)",params)
    conn.commit()

# 게시글 목록 불러오기
def sugg_list():
    cur.execute('SELECT author, title, comment, date, status FROM suggestion ORDER BY date DESC')
    sugg = cur.fetchall()
    return sugg

# 검색(작성자명)
def get_by_author(author):
	cur.execute("SELECT author, title, date, comment, status FROM suggestion WHERE author like '%{}%'".format(author))
	data = cur.fetchall()
	return data
# 검색(제목)
def get_by_title(title):
	cur.execute("SELECT author, title, date, comment, status FROM suggestion WHERE title like '%{}%'".format(title))
	data = cur.fetchall()
	return data
# 검색(내용)
def get_by_comment(comment):
	cur.execute("SELECT author, title, date, comment, status FROM suggestion WHERE comment like '%{}%'".format(comment))
	data = cur.fetchall()
	return data

# 관리자 - 처리상태 수정
def admin_complete(author, title):
    cur.execute('UPDATE suggestion SET status = "처리완료" WHERE author="{}" AND title="{}"'.format(author, title))
    conn.commit()
def admin_recover(author, title):
    cur.execute('UPDATE suggestion SET status = "접수" WHERE author="{}" AND title="{}"'.format(author, title))
    conn.commit()
# 관리자 - 게시글 삭제
def admin_delete(author, title):
    cur.execute('DELETE FROM suggestion WHERE author="{}" AND title="{}"'.format(author, title))
    conn.commit()
    # conn.close()


# 게시글 수정/삭제
def update_sugg(title, comment, author, pword):
    cur.execute('UPDATE suggestion SET title="{}", comment="{}" WHERE author="{}" AND pword="{}"'.format(title, comment, author, pword))
    conn.commit()
def delete_sugg(author, pword, title):
    cur.execute('DELETE FROM suggestion WHERE author="{}" AND pword="{}" AND title="{}"'.format(author,pword,title))
    conn.commit()


# ▲ DB 관련 
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------

def run_suggestions():

    """
    건의사항 탭의 함수입니다
    :parameter:
    :return:
    """

    st.subheader('건의사항')

    # 문의사항 입력
    with st.expander("문의하기"):
        sugg_tab1, sugg_tab2 = st.tabs(["글 등록", "수정/삭제"]) 
        with sugg_tab1:
            form_submit = st.form(key="submit")
            with form_submit:
                create_tb()
                cols = st.columns((1,1))
                author = cols[0].text_input("작성자명 ", max_chars = 12)
                pword = cols[1].text_input("비밀번호", type = "password")
                email = st.text_input("이메일")
                title = st.text_input("제목", max_chars = 50)
                comment = st.text_area("내용 ")
                date = time.strftime('%Y.%m.%d %H:%M:%S')
                status = "접수"
                submit = st.form_submit_button(label="작성")
                # 문의사항 접수
                if submit:
                    if author == "" or pword == "" or email == "" or title == "" or comment == "":
                        st.error('빈칸을 확인해주세요.')
                    else:
                        add_data(author, pword, email, title, comment, date, status)
                        st.success("문의하신 내용이 접수되었습니다! 답변은 이메일로 발송됩니다. 감사합니다.")


        # 수정/삭제 (관리자 및 사용자)
        with sugg_tab2:
            form_update = st.form(key="update")
            with form_update:
                st.markdown("_삭제시에는 삭제할 게시물의 **작성자명과 비밀번호, 제목**을 입력해주세요_")
                cols = st.columns((1,1))
                author = cols[0].text_input("작성자명", max_chars = 12)
                pword = cols[1].text_input("비밀번호", type = "password")
                # email = st.text_input("이메일")
                title = st.text_input("제목", max_chars = 50)
                comment = st.text_area("내용 ")
                cols = st.columns((1,1,1,1,1,1,1,1))
                if cols[0].form_submit_button("수정"):
                    if pword == "ok_myroomadmin" :
                        admin_complete(author, title)
                    elif pword == "no_myroomadmin" :
                        admin_recover(author, title)
                    else :
                        update_sugg(title, comment, author, pword)
                if cols[1].form_submit_button("삭제"):
                    if pword == "del_myroomadmin":
                        admin_delete(author, title)
                    else :
                        delete_sugg(author, pword, title)
 

     # 검색
    with st.expander("검색"):
        cols = st.columns((1,1))
        search_term = cols[0].text_input(' ')
        search_option = cols[1].selectbox(" ",("--검색옵션--","내용","작성자명","제목"))
        if st.button("검색"):
                if search_term == "":
                    st.warning("검색어를 입력하세요")
                elif search_option == "내용":
                    result=get_by_comment(search_term)
                    s_result = pd.DataFrame(result, columns=['작성자명', '제목', '내용', '작성시각', '상태'])
                    st.dataframe(s_result, use_container_width=True)
                elif search_option =="작성자명":
                    result=get_by_author(search_term)
                    s_result = pd.DataFrame(result, columns=['작성자명', '제목', '내용', '작성시각', '상태'])
                    st.dataframe(s_result, use_container_width=True)
                elif search_option =="제목":
                    result=get_by_title(search_term)
                    s_result = pd.DataFrame(result, columns=['작성자명', '제목', '내용', '작성시각', '상태'])
                    st.dataframe(s_result, use_container_width=True)
                else :
                    st.warning("검색옵션을 입력하세요")


    # 목록
    tab1, tab2 = st.tabs(["자주 묻는 질문", "목록"])

    with tab1:
        st.markdown("**_아래는 예시_**")

        if st.checkbox("📈전세예측 조회 방법"):
            st.markdown('''
                        > **전세예측 조회방법**
                        1. 전세예측 탭을 클릭한다 
                        2. 전세/월세 그래프 중 하나를 선택한다
                        ''')
        if st.checkbox("🔎전월세 검색 방법"):
            st.markdown('''
                        > **전월세 검색 방법**
                        1. 전월세 검색 탭을 클릭한다
                        2. ······.
                        3. ······.
                        ''')
            # st.image('https://images.mypetlife.co.kr/content/uploads/2018/12/09154907/cotton-tulear-2422612_1280.jpg', width = 600)

    with tab2:
        list = sugg_list()
        # st.write(list)
        df = pd.DataFrame(list, columns=['작성자명', '제목', '내용', '작성시각', '상태'])
        st.dataframe(df, use_container_width=True)
