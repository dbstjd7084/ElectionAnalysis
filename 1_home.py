import streamlit as st
import time

# 페이지 설정
st.set_page_config(
    page_title="2025 대선 후보자 분석", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 후보자 목록
candidates = [
    {
        "name": "이재명", 
        "image": "https://cdn.nec.go.kr/photo_20250603/Gsg1/Hb100153692/gicho/thumbnail.100153692.JPG",
        "party": "더불어민주당",
        "color": "#1f77b4"
    },
    {
        "name": "김문수", 
        "image": "https://cdn.nec.go.kr/photo_20250603/Gsg1/Hb100153710/gicho/thumbnail.100153710.JPG",
        "party": "국민의힘",
        "color": "#d62728"
    },
    {
        "name": "이준석", 
        "image": "https://cdn.nec.go.kr/photo_20250603/Gsg1/Hb100153689/gicho/thumbnail.100153689.JPG",
        "party": "개혁신당",
        "color": "#ff7f0e"
    },
    {
        "name": "권영국", 
        "image": "https://cdn.nec.go.kr/photo_20250603/Gsg1/Hb100153725/gicho/thumbnail.100153725.JPG",
        "party": "민주노동당",
        "color": "#dbdd47"
    },
    {
        "name": "황교안", 
        "image": "https://cdn.nec.go.kr/photo_20250603/Gsg1/Hb100153708/gicho/thumbnail.100153708.JPG",
        "party": "무소속",
        "color": "#a3a3a3"
    },
    {
        "name": "송진호", 
        "image": "https://cdn.nec.go.kr/photo_20250603/Gsg1/Hb100153722/gicho/thumbnail.100153722.JPG",
        "party": "무소속",
        "color": "#a3a3a3"
    },
]

st.markdown("""
<style>
.candidate-card {
    aspect-ratio: 3/4;
    background-position: center;
    background-size: cover;
    position: relative;
    overflow: hidden;
    margin: 10px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    border: 2px solid transparent;
    transition: all 0.3s ease;
    min-height: 260px;
    display: flex;
    align-items: flex-end;

}
.candidate-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
}
.candidate-overlay {
    position: absolute;
    left: 0; top: 0; right: 0; bottom: 0;
    width: 100%; height: 100%;
    background: rgba(0,0,0,0.45);   /* 여기서 투명도 조절! */
    display: flex;
    flex-direction: column;
    justify-content: flex-end; /* 내용이 아래에 위치하도록 */
    padding: 0;
    z-index: 2;
}
.candidate-info-area {
    width: 100%;
    padding: 24px 12px 18px 12px;
    box-sizing: border-box;
    background: linear-gradient(to top, rgba(0,0,0,0.55) 80%, rgba(0,0,0,0.01) 100%);
    border-radius: 0 0 15px 15px;
}
.candidate-name {
    color: #fff;
    font-weight: bold;
    font-size: 1.25rem;
    margin-bottom: 10px;
    text-align: center;
}
.party-label {
    background: var(--party-color, #aaa);
    color: #fff;
    font-weight: 500;
    border-radius: 9px;
    padding: 1.5px 6px;
    font-size: 0.9rem;
    display: inline-block;
    min-width: 55px;
    text-align: center;
    margin: 0 auto;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)


# 메인 헤더
st.markdown('<h1 class="header-title">🌟 2025 대한민국 대선 후보자 분석 🌟</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1rem; color: white; margin-bottom: 2rem;'>각 후보자를 클릭하여 상세 정보를 확인하세요</p>", unsafe_allow_html=True)

# 후보자 목록 섹션
st.markdown("### 후보자 목록")

# 후보자 카드를 3열로 배치
cols = st.columns([1, 0.3, 1, 0.3, 1])  # 카드 3개, 사이 여백 2개

for idx, candidate in enumerate(candidates):
    col_idx = idx % 3
    col_num = col_idx * 2  # 0, 2, 4
    with cols[col_num]:
        bg_image = candidate['image']
        party_color = candidate['color']
        st.markdown(f"""
        <div class="candidate-card" style="background-image: url('{bg_image}');">
            <div class="candidate-overlay">
                <div class="candidate-info-area">
                    <span class="candidate-name">{candidate['name']}</span>
                    <span class="party-label" style="background:{party_color};">{candidate['party']}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"{candidate['name']} 후보 분석", key=f"btn_{idx}", use_container_width=True):
            st.session_state["selected_candidate"] = candidate
            st.switch_page("pages/2_candidate_page.py")


# --- 여기부터 공약 요약 섹션---

# 후보별 요약 데이터
summaries = {
    "이재명": [
        "기본소득 도입을 통한 사회안전망 구축",
        "청년 일자리 100만개 창출 정책",
        "의료 공공성 강화 및 전국민 건강보험 확대",
        "탄소중립 달성을 위한 그린뉴딜 정책"
    ],
    "김문수": [
        "규제 혁신을 통한 기업 활동 지원",
        "4차 산업혁명 대응 인재양성 시스템 구축",
        "부동산 정책 정상화 및 주택공급 확대",
        "국방력 강화를 통한 안보 체제 구축"
    ],
    "이준석": [
        "디지털 정부 구현을 통한 행정 혁신",
        "젊은 세대를 위한 정치 개혁",
        "스타트업 생태계 조성 및 벤처 투자 확대",
        "교육 시스템 혁신 및 미래인재 양성"
    ],
    "권영국": [
        "노동자 권익 보호 및 근로조건 개선",
        "사회적 약자를 위한 복지 정책 확대",
        "환경 보호 및 지속가능한 발전 정책",
        "평화통일을 위한 대북 정책 추진"
    ],
    "황교안": [
        "전통적 가치 보존 및 사회 안정성 확보",
        "국가 정체성 강화 및 애국교육 확대",
        "법치주의 확립 및 공정사회 구현",
        "안보 중심의 외교 정책 추진"
    ],
    "송진호": [
        "시민 중심의 정치 개혁",
        "지역 균형 발전 및 분권화 정책",
        "중소기업 지원 및 자영업자 보호",
        "투명하고 청렴한 정부 구현"
    ]
}

st.markdown("---")
st.markdown("### 후보자별 공약 요약")

# 후보자 공약 요약 열기 상태 관리
if "summary_shown" not in st.session_state:
    st.session_state.summary_shown = False
if "opened_idx" not in st.session_state:
    st.session_state.opened_idx = None

# 분석 버튼
if not st.session_state.summary_shown:
    if st.button("🤖 AI 공약 분석 시작", use_container_width=True):
        with st.spinner("AI가 후보자 공약을 분석하고 있습니다..."):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
        st.session_state.summary_shown = True

# 후보자별 공약 요약 리스트 (분석 후만 노출)
if st.session_state.summary_shown:
    for idx, candidate in enumerate(candidates):
        row = st.columns([1, 6])
        with row[0]:
            st.markdown(
                f'<img src="{candidate["image"]}" width="65" style="margin: 10px">',
                unsafe_allow_html=True
            )
        with row[1]:
            # 후보자별 토글 버튼
            if st.button(f"{candidate['name']} ({candidate['party']})", key=f"toggle_{idx}", use_container_width=True):
                # 같은 idx 클릭 시 닫힘
                if st.session_state.opened_idx == idx:
                    st.session_state.opened_idx = None
                else:
                    st.session_state.opened_idx = idx

            # 토글 상태면 요약 펼침
            if st.session_state.opened_idx == idx:
                st.markdown(
                    "<ul style='margin-bottom:20px;'>"
                    + "".join([f"<li>{item}</li>" for item in summaries.get(candidate['name'], ["공약 정보 없음"])])
                    + "</ul>",
                    unsafe_allow_html=True
                )
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("👆 [AI 공약 분석 시작] 버튼을 누르면 후보자별 요약이 나옵니다.")

# 푸터
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <p>📊 데이터 기반 선거 정보 서비스 | 🤖 AI 기술 활용</p>
    <p style='font-size: 0.8rem; opacity: 0.7;'>
        ※ 본 서비스는 공정한 선거 정보 제공을 목적으로 합니다.
    </p>
</div>
""", unsafe_allow_html=True)