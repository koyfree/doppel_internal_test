import streamlit as st
import pandas as pd

# 구글시트에서 CSV 읽기 (전체공개 설정 시 작동)
CSV_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1dbYNM6ICiKlLGwZUQbl_zB2pKWe49tYrqOun_k5I6h8"
    "/export?format=csv"
)

# 세션 단계 초기화
if "step" not in st.session_state:
    st.session_state.step = "select"

# 프로필 불러오기
@st.cache_data
def load_profiles():
    df = pd.read_csv(CSV_URL)
    profiles = {}
    for _, row in df.iterrows():
        name = row["Name"]
        profile_text = (
            "Profile:\n\n"
            "[Demographics]\n" + str(row["Demo"]) + "\n\n"
            "[Personality]\n" + str(row["Big5"]) + "\n\n"
            "[Top 5 Things this character loves and hates]\n"
            + "• What this character love: " + str(row["top5_love"]) + "\n"
            + "• What this character hate: " + str(row["top5_hate"]) + "\n\n"
            "[Weekly Activities Overview]\n"
            + "• " + str(row["weekly_activities"])
        )
        profiles[name] = profile_text
    return profiles

# STEP 1: 조건 선택
if st.session_state.step == "select":
    st.title("실험 조건 선택")

    profiles = load_profiles()
    user_name = st.selectbox("이름을 선택하세요:", list(profiles.keys()))

    if user_name:
        st.markdown("#### 🧾 당신의 프로필")
        st.code(profiles[user_name])

        chatbot_type = st.radio("챗봇 유형을 선택하세요:", ["도플갱어 챗봇", "일반 챗봇"])
        topic = st.radio("대화 주제를 선택하세요:", ["정신 건강", "관계 갈등"])
        language = st.radio("언어를 선택하세요:", ["한국어", "영어"])

        if st.button("다음"):
            st.session_state.update({
                "user_name": user_name,
                "profile": profiles[user_name],
                "chatbot_type": chatbot_type,
                "topic": topic,
                "language": language,
                "step": "chat"
            })
            st.rerun()

# STEP 2: 단일 chatbot 모듈 실행
elif st.session_state.step == "chat":
    import chatbot  # 단일 챗봇 모듈

    chatbot.run(
        user_name=st.session_state.user_name,
        profile=st.session_state.profile,
        chatbot_type=st.session_state.chatbot_type,
        topic=st.session_state.topic,
        language=st.session_state.language
    )
