import streamlit as st
from candidate_summary import get_gemini_summary

# 후보자 목록
candidates = [
    {"name": "이재명", "image": "https://cdn.nec.go.kr/photo_20250603/Gsg1/Hb100153692/gicho/thumbnail.100153692.JPG"},
    {"name": "김문수", "image": "https://cdn.nec.go.kr/photo_20250603/Gsg1/Hb100153710/gicho/thumbnail.100153710.JPG"},
    {"name": "이준석", "image": "https://cdn.nec.go.kr/photo_20250603/Gsg1/Hb100153689/gicho/thumbnail.100153689.JPG"},
    {"name": "권영국", "image": "https://cdn.nec.go.kr/photo_20250603/Gsg1/Hb100153725/gicho/thumbnail.100153725.JPG"},
    {"name": "황교안", "image": "https://cdn.nec.go.kr/photo_20250603/Gsg1/Hb100153708/gicho/thumbnail.100153708.JPG"},
    {"name": "송진호", "image": "https://cdn.nec.go.kr/photo_20250603/Gsg1/Hb100153722/gicho/thumbnail.100153722.JPG"},
]

st.set_page_config(page_title="2025 대선 후보자 분석석", layout="wide")
st.title("🌟 2025 대한민국 대선 후보자 분석 🌟")
st.markdown("---")

st.subheader("후보자 목록")
cols = st.columns(len(candidates), gap="small")
for idx, c in enumerate(candidates):
    with cols[idx]:
        st.image(c["image"], width=150)
        if st.button(c["name"], key=f"btn_{idx}"):
            st.session_state["selected_candidate"] = c["name"]
            st.switch_page("2_candidate_page.py")

st.markdown("---")
st.subheader("📌 후보자별 공약 요약")

with st.spinner("Gemini 요약 중..."):
    try:
        summary_text = get_gemini_summary(candidates)
        st.markdown(summary_text)
    except Exception as e:
        st.error(f"요약 실패: {e}")