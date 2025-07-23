import streamlit as st
import time
from openai import OpenAI

# 👉 메시지 렌더링 함수
def render_message(speaker, msg):
    if speaker == "🤖":
        icon = "🤖"
        align = "chat-left"
        bubble = "bot-bubble"
    else:
        icon = "👤"
        align = "chat-right"
        bubble = "user-bubble"

    html = f"""
    <div class="chat-container {align}">
        <div class="chat-bubble {bubble}">
            <span class="icon">{icon}</span> {msg}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# 👉 프롬프트 로딩 함수
def load_prompt(chatbot_type, topic, language, profile):
    type_key = "dpl" if chatbot_type == "도플갱어 챗봇" else "gen"
    topic_key = "mtl" if topic == "정신 건강" else "rel"
    lang_key = "kor" if language == "한국어" else "eng"
    path = f"prompts/{lang_key}/{type_key}_{topic_key}.txt"

    try:
        with open(path, "r", encoding="utf-8") as f:
            base_prompt = f.read()
    except FileNotFoundError:
        base_prompt = "[ERROR] No Prompt File"

    return base_prompt.strip() + "\n\n---------------------\nKnowledge Section:\n" + profile

# 👉 메인 실행 함수
def run(user_name, profile, chatbot_type, topic, language):
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])

    st.markdown("""
<style>
body, div, span, input, textarea {
    font-family: "Noto Sans", "Noto Color Emoji", "Apple Color Emoji", "Segoe UI Emoji", sans-serif !important;
}
.chat-container {
    display: flex;
    margin: 6px 0;
}
.chat-bubble {
    padding: 10px 14px;
    border-radius: 12px;
    font-size: 16px;
    line-height: 1.5;
    max-width: 80%;
}
.chat-left {
    justify-content: flex-start;
}
.chat-right {
    justify-content: flex-end;
    text-align: right;
}
.bot-bubble {
    background-color: #e3f2fd;
    color: #484848;
}
.user-bubble {
    background-color: #fcf0c5;
    color: #484848;
}
.icon {
    font-size: 16px;
    margin-right: 8px;
    margin-top: 3px;
}
</style>
""", unsafe_allow_html=True)
    

    # 세션 상태 초기화
    for key, default in {
        "messages": [],
        "chat_history": [],
        "intro_done": False,
        "awaiting_response": False,
        "pending_user_input": None
    }.items():
        if key not in st.session_state:
            st.session_state[key] = default

    st.title("🧠 AITwinBot 대화 시작")

    # ✅ 인트로 메시지 & 첫 응답
    if not st.session_state.intro_done:
        intro_messages = [
            f"{user_name}, Hi! I’m your AI TwinBot, created based on your data. Nice to meet you!",
            "Before we really get started, let me briefly explain how our conversation will go.",
            "I’ll ask you a few questions about a specific topic. Based on your answers, I’ll share my thoughts on that topic in three parts.",
            "It’d be great if you could give me some feedback along the way on how I’m doing!",
            "Once our conversation is over, I’ll share a link to a follow-up survey—please be sure to check it out!",
            "Alright, let’s get started! 😊"
        ]
        for msg in intro_messages:
            st.session_state.chat_history.append(("🤖", msg))
            render_message("🤖", msg)
            time.sleep(0.5)

        full_prompt = load_prompt(chatbot_type, topic, language, profile)
        st.session_state.messages.append({"role": "system", "content": full_prompt})

        with st.spinner("🤖 Twinbot is typing now..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4.1",
                    messages=st.session_state.messages,
                    temperature=1,
                    max_tokens=2048
                )
                first_reply = response.choices[0].message.content
            except Exception as e:
                first_reply = f"[ERROR] Fail to respond: {e}"

        st.session_state.chat_history.append(("🤖", first_reply))
        st.session_state.messages.append({"role": "assistant", "content": first_reply})
        render_message("🤖", first_reply)

        st.session_state.intro_done = True
        st.rerun()

    # ✅ 이전 대화 렌더링
    for speaker, msg in st.session_state.chat_history:
        render_message(speaker, msg)

    # ✅ 사용자 입력 감지 및 처리
    user_input = st.chat_input("Enter your message.")
    if user_input:
        st.session_state.pending_user_input = user_input
        st.rerun()

    # ✅ 사용자 입력 → 렌더링
    if st.session_state.pending_user_input and not st.session_state.awaiting_response:
        msg = st.session_state.pending_user_input
        st.session_state.chat_history.append(("👤", msg))
        st.session_state.messages.append({"role": "user", "content": msg})
        render_message("👤", msg)

        st.session_state.pending_user_input = None
        st.session_state.awaiting_response = True
        st.rerun()

    # ✅ 챗봇 응답 처리
    if st.session_state.awaiting_response:
        with st.spinner("🤖 Twinbot is typing now..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4.1",
                    messages=st.session_state.messages,
                    temperature=1,
                    max_tokens=2048
                )
                reply = response.choices[0].message.content
            except Exception as e:
                reply = f"[ERROR] Fail to respond: {e}"

        st.session_state.chat_history.append(("🤖", reply))
        st.session_state.messages.append({"role": "assistant", "content": reply})
        render_message("🤖", reply)

        st.session_state.awaiting_response = False
        st.rerun()
