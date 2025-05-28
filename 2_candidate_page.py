import streamlit as st
import matplotlib.pyplot as plt
from news_api import Naver_API

candidate = st.session_state.get("selected_candidate", "홍길동")
st.title(f"🎙️ {candidate} 후보자 상세 페이지")
st.markdown("---")

# AI Chat
st.subheader("🤖 AI Chatbot")
if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state["messages"]:
    st.chat_message("user").write(msg["user"])
    st.chat_message("ai").write(msg["ai"])

user_input = st.chat_input(f"{candidate} 후보자에게 질문해보세요!")
if user_input:
    ai_response = f"'{candidate}' 후보의 AI 답변 (예시)"
    st.session_state["messages"].append({"user": user_input, "ai": ai_response})
    st.experimental_rerun()

# 10대 공약
st.markdown("---")
st.subheader("📃 10대 공약 (예시)")
for i in range(1, 11):
    st.markdown(f"**{i}. {candidate}의 공약 {i}**")

# 여론 그래프
st.markdown("---")
st.subheader("📊 여론 현황")
labels = ['긍정', '부정', '중립']
sizes = [45, 35, 20]
fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
st.pyplot(fig)

# 뉴스
st.markdown("---")
st.subheader("📰 최근 뉴스 기사")
news_df = Naver_API(candidate + " 대선 공약", 5)
if not news_df.empty:
    for idx, row in news_df.iterrows():
        st.markdown(f"### [{row['Title']}]({row['Link']})")
        st.markdown(f"{row['Description']}  \n> {row['Content'][:200]}...")
        st.markdown("---")
else:
    st.info("뉴스 기사가 없습니다.")
