import streamlit as st
import pandas as pd
from knowledge_builder import build_knowledge_dict, build_knowledge_dict_sp

# 구글시트에서 CSV 읽기 (전체공개 설정 시 작동)
SHEET_URL = (
    "https://docs.google.com/spreadsheets/d/1dbYNM6ICiKlLGwZUQbl_zB2pKWe49tYrqOun_k5I6h8/edit?usp=sharing"
)

# 세션 단계 초기화
if "step" not in st.session_state:
    st.session_state.step = "select"

# 프로필 불러오기
@st.cache_data
def load_profiles_org():
    return build_knowledge_dict(SHEET_URL)

@st.cache_data
def load_profiles_split():
    return build_knowledge_dict_sp(SHEET_URL)

# STEP 1: 조건 선택
if st.session_state.step == "select":
    st.title("실험 조건 선택")

    profiles = load_profiles_org()
    raw_names = list(profiles.keys())
    name_options = ["--- 이름을 선택하세요 ---"] + raw_names
    user_name = st.selectbox("이름을 선택하세요:", name_options)

    if user_name != "--- 이름을 선택하세요 ---":
        chatbot_type = st.radio("챗봇 유형을 선택하세요:", ["도플갱어 챗봇"])
        topic = st.radio("대화 주제를 선택하세요:", ["정신 건강", "관계 갈등"])
        model = st.radio("모델을 선택하세요:", ["② GPT-4.1(분리)", "④ GPT-5(분리)"])
        
        if model in ["④ GPT-5(분리)", "② GPT-4.1(분리)"]:
            profiles = load_profiles_split()
        else:
            profiles = load_profiles_org()
               
        if st.button("프로필 보기"):
            st.code(profiles[user_name])
    
        if st.button("다음"):
            st.session_state.update({
                "user_name": user_name,
                "profile": profiles[user_name],
                "chatbot_type": chatbot_type,
                "topic": topic,
                "model": model,
                "step": "chat"
            })
            st.rerun()

# STEP 2: 단일 chatbot 모듈 실행
elif st.session_state.step == "chat":  
    if st.session_state.model == "① GPT-4.1(원래)":
        import chatbot_gpt4_org as app
    elif st.session_state.model == "② GPT-4.1(분리)":
        import chatbot_gpt4_sp as app
    elif st.session_state.model == "③ GPT-5(원래)":
        import chatbot_gpt5_org as app
    elif st.session_state.model == "④ GPT-5(분리)":
        import chatbot_gpt5_sp as app

    app.run(
        user_name=st.session_state.user_name,
        profile=st.session_state.profile,
        chatbot_type=st.session_state.chatbot_type,
        topic=st.session_state.topic,
        language="eng"
    )
