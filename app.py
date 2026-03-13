import streamlit as st
import google.generativeai as genai

# 1. 웹사이트 기본 설정
st.set_page_config(page_title="탐구비서", page_icon="🧪", layout="wide")

# UI 정리: 가족 전용 느낌 물씬 나게!
st.title("🧪 태연이네 가족 비밀 탐구소")
st.markdown("---")

# 2. 사이드바 설정 (비밀 창고에서 열쇠 자동 가져오기)
if 'model' not in st.session_state:
    st.session_state.model = None

with st.sidebar:
    st.header("🔑 AI 엔진 상태")
    try:
        # 스트림릿 비밀 창고(Secrets)에서 열쇠를 가져와!
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        
        # 사용 가능한 최신 모델 자동 탐색
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target_model = next((m for m in models if 'flash' in m), models[0])
        
        # 구글 검색 도구 탑재 (2026 표준 방식)
        st.session_state.model = genai.GenerativeModel(
            model_name=target_model,
            tools=[{"google_search": {}}]
        )
        st.success("가족 전용 열쇠로 자동 연결됐어! ✅")
        st.info(f"현재 엔진: {target_model}")
    except Exception as e:
        st.error("비밀 창고에 열쇠가 없어! 스트림릿 설정을 확인해줘.")
        st.write(f"에러 내용: {e}")

# 3. 5단계 탭 구성
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 1. 자료조사", 
    "📰 2. 뉴스 검색 및 요약", 
    "💡 3. 가설설정", 
    "📄 4. 탐구보고서 개요",
    "✨ 5. 탐구보고서 완성"
])

# --- Step 1. 자료조사 ---
with tab1:
    st.header("🔍 Step 1. 자료조사")
    topic = st.text_input("탐구 주제를 입력하세요.", key="topic_input")
    if st.button("자료 검색 시작", key="btn1"):
        if st.session_state.model and topic:
            with st.spinner('🚀 AI가 주제 관련 최신 데이터를 분석 중입니다...'):
                response = st.session_state.model.generate_content(f"'{topic}'에 대한 최신 이슈와 주요 개념을 3가지로 정리해줘.")
                st.info(f"### 🔍 자료조사 결과\n\n{response.text}")
        else:
            st.error("주제를 입력해주세요!")

# --- Step 2. 뉴스 검색 및 요약 ---
with tab2:
    st.header("📰 Step 2. 실시간 뉴스 검색 및 요약")
    if st.button("최신 실제 기사 가져오기", key="get_real_news"):
        if st.session_state.model and topic:
            with st.spinner(f'🗞️ AI가 {topic} 관련 뉴스 기사를 검색 중입니다...'):
                prompt = f"'{topic}'과 관련된 최신 뉴스 기사의 제목, 언론사, 내용을 상세히 알려줘."
                response = st.session_state.model.generate_content(prompt)
                st.session_state.news_text = response.text
                st.success("기사를 성공적으로 가져왔습니다.")
        else:
            st.error("주제를 먼저 입력해주세요!")

    current_text = st.session_state.get('news_text', "")
    long_text = st.text_area("가져온 기사 전문", value=current_text, height=250)
    
    if st.button("기사 핵심 요약", key="btn2"):
        if st.session_state.model and long_text:
            with st.spinner('📝 기사 내용을 정밀하게 요약하고 있습니다...'):
                response = st.session_state.model.generate_content(f"다음 기사를 3줄 요약해줘:\n\n{long_text}")
                st.info(f"### 📋 요약 결과\n\n{response.text}")

# --- Step 3. 가설설정 ---
with tab3:
    st.header("💡 Step 3. 가설설정")
    if st.button("탐구 가설 추천", key="btn3"):
        if st.session_state.model and topic:
            with st.spinner('🤔 창의적인 탐구 가설을 설계하고 있습니다...'):
                response = st.session_state.model.generate_content(f"'{topic}' 주제에 맞는 중학생 수준 탐구 가설 3가지를 추천해줘.")
                st.info(f"### 💡 추천 가설\n\n{response.text}")

# --- Step 4. 탐구보고서 개요 ---
with tab4:
    st.header("📄 Step 4. 탐구보고서 개요")
    if st.button("탐구보고서 개요 생성", key="btn4"):
        if st.session_state.model and topic:
            with st.spinner('✍️ 탐구의 흐름을 잡기 위한 개요를 작성 중입니다...'):
                prompt = f"'{topic}' 주제로 1.동기 2.과정 3.결과 4.배움 구조의 보고서 개요를 작성해줘."
                response = st.session_state.model.generate_content(prompt)
                st.info(f"### 📄 보고서 개요\n\n{response.text}")

# --- Step 5. 탐구보고서 완성 ---
with tab5:
    st.header("✨ Step 5. 탐구보고서 완성")
    if st.button("최종 서술형 보고서 완성", key="btn5"):
        if st.session_state.model and topic:
            with st.spinner('🎊 모든 자료를 통합하여 정식 서술형 보고서와 출처를 정리 중입니다...'):
                prompt = f"""
                탐구 주제: {topic}
                위 주제를 바탕으로 학교 제출용 정식 서술형 보고서를 작성해줘. 
                1. 동기, 과정, 결과, 느낀 점을 포함하여 자연스럽게 이어지는 에세이 형식으로 작성할 것.
                2. 중학생이 쓴 것처럼 생생한 표현을 사용하고, 전체 문맥이 매끄럽게 연결되도록 할 것.
                3. **반드시 마지막에 [참고 문헌 및 출처] 항목을 만들어 검색된 기사 제목이나 정보 출처를 명시할 것.**
                """
                response = st.session_state.model.generate_content(prompt)
                st.success("최종 탐구보고서가 완성되었습니다!")
                st.text_area("최종 보고서 전문", response.text, height=500)
                st.download_button("💾 보고서 파일(TXT) 저장", response.text, file_name=f"{topic}_탐구보고서.txt")
