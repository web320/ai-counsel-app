import streamlit as st
from datetime import datetime
import os
from openai import OpenAI
from dotenv import load_dotenv

# 환경변수 불러오기
load_dotenv()
client = OpenAI(api_key=os.getenv("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"))

# 최대 상담 횟수 설정
MAX_FREE_USAGE = 7

# 세션 상태 초기화
if "usage_count" not in st.session_state:
    st.session_state.usage_count = 0
if "last_day" not in st.session_state:
    st.session_state.last_day = datetime.now().date()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "feedback" not in st.session_state:
    st.session_state.feedback = []

# 날짜가 바뀌면 사용 횟수 초기화
if st.session_state.last_day != datetime.now().date():
    st.session_state.usage_count = 0
    st.session_state.last_day = datetime.now().date()
    st.session_state.chat_history = []
    st.session_state.feedback = []

# GPT-4 응답 함수
def get_gpt_response(user_input):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "넌 따뜻한 여자 상담사야. 불필요한 위로나 조언은 하지 않고, 사용자의 이익이 되도록 진심으로 대답해줘."},
                {"role": "user", "content": user_input},
            ],
            temperature=0.7,
            max_tokens=600,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"오류가 발생했어요: {e}"

# 앱 UI
st.markdown("### 🔐 오늘 남은 무료 상담: **{}회 / {}회**".format(MAX_FREE_USAGE - st.session_state.usage_count, MAX_FREE_USAGE))
st.markdown("---")

# 사용자 입력 받기
user_input = st.text_input("**AI에게 고민을 털어놓기...**")

if st.button("🧠 상담 시작") and user_input:
    if st.session_state.usage_count < MAX_FREE_USAGE:
        ai_response = get_gpt_response(user_input)
        st.session_state.chat_history.append(("나", user_input))
        st.session_state.chat_history.append(("AI", ai_response))
        st.session_state.usage_count += 1
    else:
        st.error("⚠️ 오늘의 무료 상담은 모두 사용했어요. 내일 다시 오거나 유료 상담을 이용해주세요.")

# 대화 내용 표시
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# 피드백 기능 추가
if st.session_state.chat_history:
    st.markdown("---")
    st.markdown("**💬 이 대화는 어땠나요?**")
    feedback = st.radio("피드백을 남겨주세요", ["좋았어요", "보통이에요", "별로였어요"], key="feedback_radio")
    if st.button("피드백 제출"):
        st.session_state.feedback.append((datetime.now().isoformat(), feedback))
        st.success("고마워요. 더 나은 상담을 위해 참고할게요.")

# 관리자용 히스토리 확인 (숨김 기능)
if "admin" in st.secrets:
    if st.secrets["admin"] == "true":
        st.markdown("---")
        st.subheader("🛠 관리자 히스토리 로그")
        st.write("대화 수:", len(st.session_state.chat_history))
        st.write("피드백 수:", len(st.session_state.feedback))
        st.json(st.session_state.feedback)

