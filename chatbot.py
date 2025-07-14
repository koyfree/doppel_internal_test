import streamlit as st
import time
from openai import OpenAI
import os

def load_prompt(chatbot_type, topic, language, profile):
    type_key = "dpl" if chatbot_type == "도플갱어 챗봇" else "gen"
    topic_key = "mtl" if topic == "정신 건강" else "rel"
    lang_key = "kor" if language == "한국어" else "eng"
    path = f"prompts/{lang_key}/{type_key}_{topic_key}.txt"

    try:
        with open(path, "r", encoding="utf-8") as f:
            template = f.read()
        return template.replace("{knowledge}", profile)
    except FileNotFoundError:
        return f"[ERROR] 프롬프트 파일 {path} 없음"

def run(user_name, profile, chatbot_type, topic, language):
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])

    # 상태 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "intro_done" not in st.session_state:
        st.session_state.intro_done = False
    if "awaiting_response" not in st.session_state:
        st.session_state.awaiting_response = False

    st.title("🧠 AITwinBot 대화 시작")

    # 인트로 메시지 4개 출력 (1회만)
    if not st.session_state.intro_done:
        intro_messages = [
            f"{user_name}님, 만나서 반가워요!",
            "이제부터 당신과 대화를 나눌 챗봇이에요.",
            "당신의 프로필 정보를 바탕으로 대화를 도와드릴게요.",
            "잠시 후 제가 먼저 말을 걸게요 😊"
        ]
        for msg in intro_messages:
            st.session_state.chat_history.append(("🤖", msg))
            st.markdown(f"**🤖** {msg}")
            time.sleep(1.0)

        # 시스템 프롬프트 삽입
        base_prompt = load_prompt(chatbot_type, topic, language)
        full_prompt = (base_prompt.strip() +
        "\n\n---------------------\nKnowledge Section:\n" +
        profile
        )
        st.session_state.messages.append({"role": "system", "content": full_prompt})

        # 챗봇 첫 응답 생성
        with st.spinner("🤖 챗봇이 인사말을 준비 중이에요..."):
            response = client.chat.completions.create(
                model="gpt-4.1",
                messages=st.session_state.messages,
                temperature=1,
                max_tokens=2048
            )
        first_reply = response.choices[0].message.content
        st.session_state.chat_history.append(("🤖", first_reply))
        st.session_state.messages.append({"role": "assistant", "content": first_reply})

        st.session_state.intro_done = True
        st.rerun()

    # 이전 대화 출력
    for speaker, msg in st.session_state.chat_history:
        st.markdown(f"**{speaker}** {msg}")

    # 사용자 입력 처리
    user_input = st.chat_input("메시지를 입력하세요")
    if user_input:
        st.session_state.chat_history.append(("👤", user_input))
        st.session_state.messages.append({"role": "user", "content": user_input})

        # 응답 생성
        with st.spinner("🤖 챗봇이 응답 중이에요..."):
            response = client.chat.completions.create(
                model="gpt-4.1",
                messages=st.session_state.messages,
                temperature=1,
                max_tokens=2048
            )
        reply = response.choices[0].message.content

        st.session_state.chat_history.append(("🤖", reply))
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()
