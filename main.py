import streamlit as st
import pandas as pd
from knowledge_builder import build_knowledge_dict

# 구글시트에서 CSV 읽기 (전체공개 설정 시 작동)
SHEET_URL = (
    "https://docs.google.com/spreadsheets/d/1dbYNM6ICiKlLGwZUQbl_zB2pKWe49tYrqOun_k5I6h8/edit?usp=sharing"
)

# 세션 단계 초기화
if "step" not in st.session_state:
    st.session_state.step = "select"

# 프로필 불러오기
@st.cache_data
def load_profiles():
    return build_knowledge_dict(SHEET_URL)

# STEP 1: 조건 선택
if st.session_state.step == "select":
    st.title("실험 조건 선택")

    profiles = load_profiles()
    raw_names = list(profiles.keys())
    name_options = ["--- 이름을 선택하세요 ---"] + raw_names
    user_name = st.selectbox("이름을 선택하세요:", name_options)

    if user_name != "--- 이름을 선택하세요 ---":
        # st.markdown("#### 🧾 당신의 프로필")
        # st.code(profiles[user_name])

        chatbot_type = st.radio("챗봇 유형을 선택하세요:", ["도플갱어 챗봇", "일반 챗봇"])
        topic = st.radio("대화 주제를 선택하세요:", ["정신 건강", "관계 갈등"])
        model = st.radio("모델을 선택하세요:", ["GPT-4.1", "Claude Sonnet 4", "Gemini 2.5 Flash"])

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
    if st.session_state.model == "GPT-4.1":
        import chatbot_gpt as app
    elif st.session_state.model == "Claude Sonnet 4":
        import chatbot_claude as app
    elif st.session_state.model == "Gemini 2.5 Flash":
        import chatbot_gemini as app

    app.run(
        user_name=st.session_state.user_name,
        profile=st.session_state.profile,
        chatbot_type=st.session_state.chatbot_type,
        topic=st.session_state.topic,
        language="eng"
    )
