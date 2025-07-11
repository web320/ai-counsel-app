import streamlit as st
from datetime import datetime
from streamlit_chat import message  # 메시지 형태 출력용 패키지 (추가 설치 필요 시 pip install streamlit-chat)
import random
import pyttsx3

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
st.markdown("""
<h1 style='text-align: center; color: #fff;'>💬 루루 AI 고민 상담소</h1>
<p style='text-align: center; color: #ccc;'>감정을 선택하고, 오늘의 속마음을 털어놔보세요.</p>
""", unsafe_allow_html=True)

# -------------------- 감정 선택 --------------------
st.markdown("## 😊 오늘 기분은?")
feeling = st.radio("감정을 선택해 주세요", ["😢 슬픔", "😨 불안", "😠 화남", "😐 무감정", "😍 설렘"], horizontal=True)

# -------------------- 고민 입력 --------------------
default_text = "오늘은 " + feeling.split()[1] + " 기분이에요..."
user_input = st.text_input("💭 고민이나 하고 싶은 말을 적어보세요", value=default_text)

# -------------------- 무료 사용 횟수 안내 --------------------
st.markdown(f"**🔓 오늘 남은 무료 상담: `{MAX_FREE_USES - st.session_state['usage_count']}`회 / {MAX_FREE_USES}회**")

# -------------------- AI 응답 시뮬레이션 --------------------
def generate_response(user_input):
    suicide_keywords = ["죽고싶", "자살", "끝내고싶"]
    if any(word in user_input for word in suicide_keywords):
        return "자살은 결코 해결이 아니에요. 당신은 소중하고, 지금 겪는 어려움은 분명 지나갈 거예요. 전문가와 꼭 상담해보세요. 💙"

    templates = [
        "'{0}'에 대해 이야기해줘서 고마워요. 당신의 마음을 이해해보려 노력할게요.",
        "그런 기분 드는 거 정말 자연스러워요. '{0}'에 대해 더 얘기해볼까요?",
        "'{0}' 때문에 많이 힘드셨죠. 같이 천천히 생각해봐요.",
        "음... '{0}'이(가) 당신 마음에 큰 영향을 주고 있네요. 루루가 곁에 있어줄게요."
    ]
    return random.choice(templates).format(user_input)

# -------------------- 음성 출력 --------------------
def speak_text(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 165)
    engine.say(text)
    engine.runAndWait()

# -------------------- 상담 시작 --------------------
if st.button("🧠 AI에게 털어놓기") and user_input.strip() != "":
    if st.session_state["usage_count"] < MAX_FREE_USES:
        st.session_state["usage_count"] += 1

        ai_response = generate_response(user_input)
        st.session_state["chat_history"].append(("user", user_input))
        st.session_state["chat_history"].append(("ai", ai_response))

        speak_text(ai_response)  # 음성 출력 추가
    else:
        st.warning("오늘의 무료 상담 횟수를 모두 사용했어요. 더 많은 상담은 곧 유료로 제공될 예정입니다.")

# -------------------- 채팅 히스토리 출력 --------------------
if st.session_state["chat_history"]:
    st.markdown("---")
    st.markdown("### 📜 오늘의 상담 기록")
    for sender, msg in st.session_state["chat_history"]:
        is_user = sender == "user"
        message(msg, is_user=is_user)

# -------------------- 마플샵 배너 --------------------
st.markdown("""
---
<div style="text-align:center; margin-top:30px;">
    <a href="https://marpple.shop/kr/ljoovye_co_kr" target="_blank">
        <button style="padding: 15px 30px; font-size: 20px; background-color:#000; color:white; border:none; border-radius:8px;">
            🎁 마플샵 ‘엘조뷔’ 바로가기
        </button>
    </a>
</div>
""", unsafe_allow_html=True)

# -------------------- 푸터 --------------------
st.markdown("""
<hr>
<p style='text-align: center; font-size: 13px; color: gray;'>이 서비스는 테스트용이며, 실제 상담이 필요한 경우 전문가의 도움을 받아주세요.</p>
""", unsafe_allow_html=True)
