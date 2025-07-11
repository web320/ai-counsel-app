# app.py
import streamlit as st
from openai import OpenAI

# 🔐 OpenAI API 키 로드
api_key = st.secrets["hello"]["key"]
client = OpenAI(api_key=api_key)

# GPT 응답 함수
def get_gpt_response(user_input):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_input}],
        temperature=0.8
    )
    return response.choices[0].message.content

# Streamlit 인터페이스
st.set_page_config(page_title="AI 고민상담소", layout="centered")
st.title("💬 AI 고민상담소")
st.write("고민을 입력하면 AI가 조언을 해줄게요.")

# 세션 상태 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 사용자 입력
user_input = st.text_input("무슨 고민이 있나요?", key="user_input")
if st.button("AI에게 물어보기") and user_input:
    try:
        ai_reply = get_gpt_response(user_input)
        st.session_state.chat_history.append((user_input, ai_reply))
    except Exception as e:
        st.error(f"오류가 발생했어요: {e}")

# 이전 대화 보여주기
if st.session_state.chat_history:
    st.subheader("📜 대화 기록")
    for q, a in reversed(st.session_state.chat_history):
        st.markdown(f"**🧍‍♀️ 너:** {q}")
        st.markdown(f"**🤖 AI:** {a}")

