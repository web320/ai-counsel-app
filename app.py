# app.py
import streamlit as st
from datetime import datetime
from openai import OpenAI
import random

# --------- OpenAI 설정 ---------
client = OpenAI(api_key="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")

# --------- 세션 상태 초기화 ---------
if "usage_count" not in st.session_state:
    st.session_state.usage_count = 0
if "last_day" not in st.session_state:
    st.session_state.last_day = datetime.now().date()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 날짜가 바뀌면 초기화
if st.session_state.last_day != datetime.now().date():
    st.session_state.usage_count = 0
    st.session_state.chat_history = []
    st.session_state.last_day = datetime.now().date()

MAX_FREE = 7

# --------- 타이틀 ---------
st.markdown("<h1 style='text-align:center;'>💬 루루 AI 고민상담소</h1>", unsafe_allow_html=True)

# --------- 감정 선택 ---------
feeling = st.radio("😊 오늘 기분은?", ["😢 슬픔", "😨 불안", "😠 화남", "😐 무감정", "😍 설렘"], horizontal=True)

# --------- 입력 ---------
default_text = f"오늘은 {feeling.split()[1]} 기분이에요..."
user_input = st.text_input("💭 고민을 적어보세요", value=default_text)

# --------- 사용 횟수 안내 ---------
st.markdown(f"**🔓 오늘 남은 무료 상담: `{MAX_FREE - st.session_state.usage_count}`회 / {MAX_FREE}회**")

# --------- GPT 응답 함수 ---------
def get_gpt_response(user_input):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "너는 감정적으로 따뜻한 고민 상담사야. 짧고 공감 가는 말로 10~30단어 이내로 응답해."},
            {"role": "user", "content": user_input}
        ],
        temperature=0.8
    )
    return response.choices[0].message.content.strip()

# --------- 버튼 클릭 시 ---------
if st.button("🧠 AI에게 털어놓기") and user_input.strip() != "":
    if st.session_state.usage_count < MAX_FREE:
        ai_response = get_gpt_response(user_input)
        st.session_state.chat_history.append(("🙋‍♀️ 나", user_input))
        st.session_state.chat_history.append(("🤖 루루", ai_response))
        st.session_state.usage_count += 1
    else:
        st.warning("오늘의 무료 상담이 모두 끝났어요. 내일 다시 찾아와 줘!")

# --------- 채팅 히스토리 출력 ---------
if st.session_state.chat_history:
    st.markdown("---")
    for sender, msg in st.session_state.chat_history:
        st.markdown(f"**{sender}:** {msg}")

# --------- 마플샵 버튼 ---------
st.markdown("""
<hr>
<div style="text-align:center;">
    <a href="https://marpple.shop/kr/ljoovye_co_kr" target="_blank">
        <button style="padding: 12px 24px; font-size: 18px; background-color:black; color:white; border:none; border-radius:8px;">
        🎁 엘조뷔 마플샵 가기
        </button>
    </a>
</div>
""", unsafe_allow_html=True)

# --------- 푸터 ---------
st.markdown("""
<p style='text-align:center; font-size:13px; color:gray;'>이 앱은 실험용입니다. 심각한 고민은 전문가에게 꼭 상담하세요.</p>
""", unsafe_allow_html=True)
