import streamlit as st
from datetime import datetime
import openai
import random

# 🔑 OpenAI API 키
openai.api_key = "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"  # 여기에 본인 API 키 입력

# -------------------- 상태 초기화 --------------------
if "usage_count" not in st.session_state:
    st.session_state["usage_count"] = 0
if "last_day" not in st.session_state:
    st.session_state["last_day"] = datetime.now().date()
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# 날짜 변경 시 카운트 초기화
today = datetime.now().date()
if st.session_state["last_day"] != today:
    st.session_state["usage_count"] = 0
    st.session_state["chat_history"] = []
    st.session_state["last_day"] = today

MAX_FREE_USES = 7

# -------------------- 타이틀 --------------------
st.markdown("<h1 style='text-align: center;'>💬 루루 ChatGPT 고민상담소</h1>", unsafe_allow_html=True)

# -------------------- 감정 선택 --------------------
feeling = st.radio("오늘 기분은 어때요?", ["😢 슬픔", "😨 불안", "😠 화남", "😐 무감정", "😍 설렘"], horizontal=True)

# -------------------- 고민 입력 --------------------
default_text = f"오늘은 {feeling.split()[1]} 기분이에요..."
user_input = st.text_input("마음 속 고민을 적어보세요", value=default_text)

st.markdown(f"**🔓 남은 무료 상담: `{MAX_FREE_USES - st.session_state['usage_count']}`회 / {MAX_FREE_USES}회**")

# -------------------- ChatGPT 응답 생성 --------------------
def get_gpt_response(user_msg):
    prompt = f"""
너는 따뜻하지만 솔직한 여자친구처럼 대답하는 감정상담가야.
사용자가 '{user_msg}' 라고 했을 때, 너무 과잉된 위로나 뻔한 조언 없이, 감정을 어루만지고, 질문을 유도하며 진심 어린 대답을 해줘.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "너는 부드러운 감성의 AI 고민상담가야."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=300
    )
    return response.choices[0].message.content.strip()

# -------------------- 상담 시작 --------------------
if st.button("🧠 AI에게 털어놓기") and user_input.strip() != "":
    if st.session_state["usage_count"] < MAX_FREE_USES:
        st.session_state["usage_count"] += 1

        ai_response = get_gpt_response(user_input)
        st.session_state["chat_history"].append(("user", user_input))
        st.session_state["chat_history"].append(("ai", ai_response))
    else:
        st.warning("오늘의 무료 상담 횟수를 모두 사용했어요.")

# -------------------- 채팅 히스토리 출력 --------------------
if st.session_state["chat_history"]:
    st.markdown("---")
    st.markdown("### 📜 상담 히스토리")
    for sender, msg in st.session_state["chat_history"]:
        if sender == "user":
            st.markdown(f"**🙋‍♀️ 나:** {msg}")
        else:
            st.markdown(f"**🤖 루루:** {msg}")
