import streamlit as st
import time
from openai import OpenAI

# 👉 스타일: 챗봇/사용자 말풍선 예쁘게 만들기
st.markdown("""
<style>
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
    color: #2e7d32;
}
.user-bubble {
    background-color: #fcf0c5;
    color: #1565c0;
}
.icon {
    font-size: 20px;
    margin-right: 8px;
    margin-top: 3px;
}
</style>
""", unsafe_allow_html=True)

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

# 👉 프롬프트 불러오기
def load_prompt(chatbot_type, topic, language):
    type_key = "dpl" if chatbot_type == "도플갱어 챗봇" else "gen"
    topic_key = "mtl" if topic == "정신 건강" else "rel"
    lang_key = "kor" if language == "한국어" else "eng"
    path = f"prompts/{lang_key}/{type_key}_{topic_key}.txt"

    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"[ERROR] 프롬프트 파일 {path} 없음"

# 👉 메인 실행 함수
def run(user_name, profile, chatbot_type, topic, language):
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])

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

    # 👉 인트로 메시지 & 첫 system prompt 설정
    if not st.session_state.intro_done:
        intro_messages = [
            f"{user_name}, 안녕! 나는 너의 데이터를 기반으로 만들어진 너의 AITwinBot이야. 만나서 반가워!",
            "본격적으로 시작하기 전에, 우리 대화가 어떻게 진행될지 간단히 설명할게.",
            "내가 특정 주제에 대해 몇 가지 물어볼게. 그걸 바탕으로, 이 주제에 대한 내 생각을 세 부분으로 나누어 얘기할거야. 마지막엔 대화가 어땠는지 평가할 수 있는 설문 링크를 알려 줄게. 꼭 참여해 줘!",
            "좋아, 그럼 시작할게! 😊"
        ]
        for msg in intro_messages:
            st.session_state.chat_history.append(("🤖", msg))
            render_message("🤖", msg)
            time.sleep(1.0)

        base_prompt = load_prompt(chatbot_type, topic, language)
        full_prompt = base_prompt.strip() + "\n\n---------------------\nKnowledge Section:\n" + profile
        st.session_state.messages.append({"role": "system", "content": full_prompt})

        # LLM 첫 응답
        with st.spinner("🤖 챗봇이 입력 중이에요..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4.1",
                    messages=st.session_state.messages,
                    temperature=1,
                    max_tokens=2048
                )
                first_reply = response.choices[0].message.content
            except Exception as e:
                first_reply = f"[ERROR] 응답 실패: {e}"

        st.session_state.chat_history.append(("🤖", first_reply))
        st.session_state.messages.append({"role": "assistant", "content": first_reply})
        st.session_state.intro_done = True
        st.rerun()

    # 👉 대화 렌더링
    for speaker, msg in st.session_state.chat_history:
        render_message(speaker, msg)

    # 👉 입력 → 입력만 받고 rerun
    user_input = st.chat_input("메시지를 입력하세요")
    if user_input:
        st.session_state.pending_user_input = user_input
        st.rerun()

    # 👉 입력 → 사용자 메시지 먼저 출력
    if st.session_state.pending_user_input and not st.session_state.awaiting_response:
        user_msg = st.session_state.pending_user_input
        st.session_state.chat_history.append(("👤", user_msg))
        st.session_state.messages.append({"role": "user", "content": user_msg})
        st.session_state.pending_user_input = None
        st.session_state.awaiting_response = True
        st.rerun()

    # 👉 챗봇 응답 생성
    if st.session_state.awaiting_response:
        with st.spinner("🤖 챗봇이 입력 중이에요..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4.1",
                    messages=st.session_state.messages,
                    temperature=1,
                    max_tokens=2048
                )
                reply = response.choices[0].message.content
            except Exception as e:
                reply = f"[ERROR] 응답 실패: {e}"

        st.session_state.chat_history.append(("🤖", reply))
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.session_state.awaiting_response = False
        st.rerun()
