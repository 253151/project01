# import the libraries
import openai
import streamlit as st
from streamlit_chat import message
import requests
openai.api_key = st.secrets['openai_credentials'].api_secret


# Creating a function which will generate the calls from the api.
def chatrun():
    """
    챗봇 탭의 함수입니다
    :parameter:
    :return:
    """
    def generate_response(prompt):
        if '부동산' in user_input:
            matching_dict = {'광진구' : '11215', '서초구' : '11650', '마포구' : '11440', '중랑구' : '11260', '구로구' : '11530',
                            '송파구' : '11710', '강남구' : '11680', '성동구' : '11200', '영등포구' : '11560', '양천구' : '11470',
                            '도봉구' : '11320', '관악구' : '11620', '중구' : '11140', '동대문구' : '11230', '노원구' : '11350',
                            '강동구' : '11740', '은평구' : '11380', '강서구' : '11500', '강북구' : '11305', '성북구' : '11290',
                            '금천구' : '11545', '동작구' : '11590', '용산구' : '11170', '서대문구' : '11410', '종로구' : '11110'}
            result = ""
            for i in matching_dict.keys():
                if i in user_input:
                    result = matching_dict[i]
            l = user_input
            s = l.split(' ')
            CNTRCT_DE = s[2]
            ACC_YEAR = s[2][:4]
            service_key = '4d42486779706d3034365957634870'
            for j in range(1,2):
                #url = f'http://openapi.seoul.go.kr:8088/{service_key}/json/tbLnOpendataRentV/{1+((j-1)*100)}/{j*100}/'+ n[0] +'/'+ result
                url = f'http://openapi.seoul.go.kr:8088/{service_key}/json/tbLnOpendataRentV/1/5/{ACC_YEAR}/{result}/ / / / / /{CNTRCT_DE}'
                print(url)
                req = requests.get(url)
                content = req.json()
                print(content)
                con = content['tbLnOpendataRentV']['row']
                a = ""
                for m in con:
                        gu = m["SGG_NM"]
                        dong = m["BJDONG_NM"]
                        day = m["CNTRCT_DE"]
                        gtn = m["RENT_GBN"]
                        price = m["RENT_GTN"]
                        a += (day +" : "+ gu + " " + dong +" "+ gtn +" "+ price +"만원\n")
                        message = a
                return message
        else:
            completions = openai.Completion.create(
            engine = "text-davinci-003",
            prompt = prompt,
            max_tokens = 1024,
            n = 1,
            stop = None,
            temperature = 0.5,
        )
            message = completions.choices[0].text
            return message
    st.subheader("💡챗봇 물어봐!")
    st.write("부동산 검색예시 - 부동산 xx구 20220101")
    # Storing the chat
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []
    def get_text():
        input_text = st.text_input("You : ","Hello, how are you?", key="input")
        return input_text
    user_input = get_text()
    if user_input:
        output = generate_response(user_input)
        #store the output
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])-1, -1,- 1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')