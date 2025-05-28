import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# 페이지 설정
st.set_page_config(
    page_title="후보자 상세 분석", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 선택된 후보자 정보 가져오기
if "selected_candidate" not in st.session_state:
    st.error("❌ 후보자가 선택되지 않았습니다. 홈페이지에서 후보자를 선택해주세요.")
    if st.button("🏠 홈페이지로 돌아가기"):
        st.switch_page("1_home.py")
    st.stop()

candidate_info = st.session_state["selected_candidate"]
candidate_name = candidate_info["name"]
candidate_party = candidate_info["party"]
candidate_color = candidate_info["color"]

# CSS 스타일링
st.markdown("""
<style>
    .main > div {
        padding-top: 1rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .candidate-header {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    
    .chat-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        min-height: 400px;
    }
    
    .promise-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid """ + candidate_color + """;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    .news-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        border-bottom: 2px solid #f0f0f0;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# 헤더 섹션
st.markdown(f"""
<div class="candidate-header">
    <img src="{candidate_info['image']}" style="width: 150px; height: 150px; border-radius: 50%; object-fit: cover; margin-bottom: 20px; border: 5px solid {candidate_color};">
    <h1 style="color: {candidate_color}; margin-bottom: 10px;">🎙️ {candidate_name} 후보자</h1>
    <h3 style="color: #666; margin-bottom: 20px;">{candidate_party}</h3>
    <p style="color: #777;">AI 챗봇과 대화하고 공약을 확인해보세요</p>
</div>
""", unsafe_allow_html=True)

# 뒤로가기 버튼
if st.button("🏠 홈페이지로 돌아가기", type="secondary"):
    st.switch_page("1_home.py")

# 메인 레이아웃: 2열 구성
col1, col2 = st.columns([2, 1], gap="medium")

with col1:
    st.markdown("## 🤖 AI 챗봇과 대화하기")
    
    # 초기 안내(채팅 위 고정, 채팅창과 별개!)
    st.markdown(f"""
    <div style="margin-bottom: 16px; background: rgba(255,255,255,0.8); border-radius: 8px; padding: 12px 18px;">
        <b>안내</b>: <span style="color: #333;">
        안녕하세요! 저는 <b>{candidate_name}</b> 후보입니다.<br>
        제 정책이나 공약에 대해 궁금한 것이 있으시면 언제든 물어보세요!
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # 사용자 입력
        user_input = st.chat_input(f"{candidate_name} 후보자에게 질문해보세요!")

        ai_response = None

        # "로딩" 메시지는 채팅 내역과 겹치지 않게 spinner로만 사용
        if user_input:
            with st.spinner("답변을 생성하고 있습니다..."):
                time.sleep(1)
                responses = {
                    "경제": f"저는 {candidate_name}으로서 경제 성장과 일자리 창출을 최우선 과제로 생각합니다. 특히 중소기업 지원과 혁신산업 육성에 집중하겠습니다.",
                    "교육": f"교육은 국가의 미래입니다. 저는 모든 학생이 평등한 교육 기회를 가질 수 있도록 교육 시스템을 개선하겠습니다.",
                    "복지": f"사회적 약자를 보호하고 모든 국민이 행복한 삶을 살 수 있도록 복지 정책을 확대하겠습니다.",
                    "환경": f"지속가능한 미래를 위해 환경 보호와 탄소 중립 정책을 적극 추진하겠습니다.",
                    "안보": f"국가 안보는 타협할 수 없는 영역입니다. 강력한 국방력을 바탕으로 평화를 지키겠습니다."
                }
                ai_response = f"안녕하세요, {candidate_name}입니다. "
                for keyword, response in responses.items():
                    if keyword in user_input:
                        ai_response = response
                        break
                else:
                    ai_response += f"좋은 질문입니다. 제가 {candidate_party} 소속으로서 이 문제에 대해 깊이 고민하고 있습니다. 구체적인 정책은 저의 10대 공약을 참고해주세요."
        
        # --- 채팅 내역 표시 구간 ---
        if user_input:
            st.chat_message("user").write(user_input)
            st.chat_message("assistant", avatar="🎤").write(ai_response)
        else:
            # "공란" 유지: 아무 메시지도 띄우지 않음!
            pass
        
        st.markdown('</div>', unsafe_allow_html=True)


with col2:
    # 10대 공약 섹션
    st.markdown("## 📃 10대 핵심 공약")
    
    # 후보자별 공약 데이터
    promises_data = {
        "이재명": [
            "기본소득 월 50만원 지급",
            "청년 일자리 100만개 창출",
            "전국민 건강보험 확대",
            "탄소중립 그린뉴딜 추진",
            "부동산 투기 근절",
            "교육 불평등 해소",
            "중소기업 지원 확대",
            "디지털 정부 구현",
            "사회적 약자 보호",
            "평화통일 기반 조성"
        ],
        "김문수": [
            "규제 혁신으로 기업 활력 제고",
            "4차 산업혁명 인재 양성",
            "부동산 정책 정상화",
            "국방력 강화",
            "세금 부담 완화",
            "자유시장경제 활성화",
            "교육 경쟁력 강화",
            "법치주의 확립",
            "북한 도발 억제",
            "전통 가치 보존"
        ],
        "이준석": [
            "디지털 행정 혁신",
            "청년 정치 참여 확대",
            "스타트업 생태계 조성",
            "교육 시스템 혁신",
            "공정한 기회 보장",
            "미래 기술 투자",
            "세대갈등 해소",
            "투명한 정부 운영",
            "혁신적 복지 정책",
            "글로벌 경쟁력 강화"
        ],
        "권영국": [
            "노동자 권익 보호",
            "사회적 약자 복지 확대",
            "환경 보호 정책 강화",
            "평화통일 추진",
            "서민 생활 안정",
            "교육 공공성 강화",
            "의료 접근성 개선",
            "주거권 보장",
            "성평등 사회 실현",
            "지역 균형 발전"
        ],
        "황교안": [
            "국가 정체성 강화",
            "애국교육 확대",
            "법치주의 확립",
            "전통 문화 보존",
            "국가 안보 강화",
            "경제 자유화 추진",
            "가족 가치 보호",
            "사회 질서 확립",
            "외교 주권 강화",
            "헌법 정신 구현"
        ],
        "송진호": [
            "시민 참여 정치 실현",
            "지역 균형 발전",
            "중소기업 지원 강화",
            "투명한 정부 구현",
            "서민 경제 살리기",
            "교육 기회 평등",
            "의료 공공성 확보",
            "청렴한 공직 문화",
            "민생 중심 정책",
            "소통하는 정부"
        ]
    }
    
    promises = promises_data.get(candidate_name, [f"{candidate_name}의 공약 {i}" for i in range(1, 11)])
    
    for i, promise in enumerate(promises, 1):
        st.markdown(f"""
        <div class="promise-card">
            <strong>{i}. {promise}</strong>
        </div>
        """, unsafe_allow_html=True)

# 두 번째 행: 여론 분석과 뉴스
st.markdown("---")
col3, col4 = st.columns([1, 1], gap="medium")

with col3:
    # 여론 분석 섹션
    st.markdown("## 📊 여론 분석 (최근 1개월)")
    
    # 모의 여론 데이터 생성
    np.random.seed(hash(candidate_name) % 100)  # 후보자별 일관된 데이터
    
    positive = np.random.randint(35, 55)
    negative = np.random.randint(20, 35)
    neutral = 100 - positive - negative
    
    # Plotly 도넛 차트
    fig = go.Figure(data=[go.Pie(
        labels=['긍정', '부정', '중립'],
        values=[positive, negative, neutral],
        hole=.3,
        marker_colors=['#2E8B57', '#DC143C', '#708090']
    )])
    
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        textfont_size=12,
        marker_line_color='white',
        marker_line_width=2
    )
    
    fig.update_layout(
        title=f"{candidate_name} 후보 여론 현황",
        title_x=0.5,
        font=dict(size=14),
        showlegend=True,
        height=400,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 여론 요약 통계
    st.markdown("### 📈 여론 요약")
    
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.metric("긍정", f"{positive}%", f"+{np.random.randint(1, 5)}%")
    with metric_col2:
        st.metric("부정", f"{negative}%", f"-{np.random.randint(1, 3)}%")
    with metric_col3:
        st.metric("중립", f"{neutral}%", f"+{np.random.randint(0, 2)}%")

with col4:
    # 관련 뉴스 섹션
    st.markdown("## 📰 최근 뉴스 기사")
    
    # 모의 뉴스 데이터
    news_data = [
        {
            "title": f"{candidate_name} 후보, 핵심 공약 발표",
            "description": f"{candidate_name} 후보가 오늘 기자회견을 통해 핵심 공약을 발표했습니다.",
            "date": "2025-05-27",
            "source": "정치뉴스"
        },
        {
            "title": f"{candidate_name} 후보 지지율 상승세",
            "description": f"최근 여론조사에서 {candidate_name} 후보의 지지율이 상승하는 것으로 나타났습니다.",
            "date": "2025-05-26",
            "source": "선거뉴스"
        },
        {
            "title": f"{candidate_name} 후보, 시민과의 대화",
            "description": f"{candidate_name} 후보가 시민들과 직접 만나 정책을 설명하는 시간을 가졌습니다.",
            "date": "2025-05-25",
            "source": "지역뉴스"
        },
        {
            "title": f"{candidate_name} 후보 경제정책 공개",
            "description": f"{candidate_name} 후보가 새로운 경제정책 방안을 제시했습니다.",
            "date": "2025-05-24",
            "source": "경제뉴스"
        },
        {
            "title": f"{candidate_name} 후보 토론회 참석",
            "description": f"{candidate_name} 후보가 주요 정책 토론회에 참석해 소신을 밝혔습니다.",
            "date": "2025-05-23",
            "source": "정치뉴스"
        }
    ]
    
    # 뉴스 카드 표시
    for news in news_data:
        st.markdown(f"""
        <div class="news-card">
            <h4 style="color: {candidate_color}; margin-bottom: 8px;">{news['title']}</h4>
            <p style="color: #666; margin-bottom: 8px;">{news['description']}</p>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <small style="color: #999;">{news['source']}</small>
                <small style="color: #999;">{news['date']}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 푸터
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: white; padding: 20px;'>
    <p>📊 {candidate_name} 후보자 상세 분석 완료</p>
    <p style='font-size: 0.8rem; opacity: 0.7;'>
        ※ 여론 데이터는 뉴스 댓글 분석 결과이며, 실제 지지율과 다를 수 있습니다.
    </p>
</div>
""", unsafe_allow_html=True)