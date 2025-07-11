from openai import OpenAI

client = OpenAI(api_key="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")  # 본인 API 키 입력

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "넌 부드러운 AI 상담가야."},
        {"role": "user", "content": "요즘 너무 불안하고 슬퍼요..."}
    ],
    temperature=0.8
)

print(response.choices[0].message.content)
import streamlit as st
from datetime import datetime
from openai import OpenAI
import random

# 🔑 OpenAI 클라이언트 세팅
client = OpenAI(api_key="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")  # 여기에 네 API 키 입력

# -------------------- 상태 초기화 --------------------
if "usage_count" not in st.session_state:
    st.session_state["usage_count"] = 0
if "last_day" not in st.session_state:
    st.session_state["last_day"] = datetime.now().date()
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

today = datetime.now().date()
if st.session_state["last_day"] != today:
    st.session_state["usage_count"] = 0
    st.session_state["chat_history"] = []
    st.session_state["last_day"] = today

MAX_FREE_USES = 7

# -------------------- UI --------------------
st.markdown("<h1 style='text-align: center;'>💬 루루 ChatGPT 고민상담소</h1>", unsafe_allow_html=True)

feeling = st.radio("오늘 기분은 어때요?", ["😢 슬픔", "😨 불안", "😠 화남", "😐 무감정", "😍 설렘"], horizontal=True)
default_text = f"오늘은 {feeling.split()[1]} 기분이에요..."
user_input = st.text_input("마음 속 고민을 적어보세요", value=default_text)

st.markdown(f"**🔓 남은 무료 상담: `{MAX_FREE_USES - st.session_state['usage_count']}`회 / {MAX_FREE_USES}회**")

# -------------------- GPT 응답 --------------------
def get_gpt_response(user_msg):
    prompt = f"""
너는 따뜻하고 솔직한 여자친구 같은 AI야. 사용자가 '{user_msg}' 라고 했을 때, 진심으로 공감해주고 위로해줘.
너무 형식적이지 말고, 심플하고 인간적인 말투로 말해줘.
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "너는 감성적인 상담가 AI야."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.85
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

# -------------------- 히스토리 출력 --------------------
if st.session_state["chat_history"]:
    st.markdown("---")
    st.markdown("### 📜 상담 히스토리")
    for sender, msg in st.session_state["chat_history"]:
        if sender == "user":
            st.markdown(f"**🙋‍♀️ 나:** {msg}")
        else:
            st.markdown(f"**🤖 루루:** {msg}")
