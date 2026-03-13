import streamlit as st
import google.generativeai as genai

# 1. 웹사이트 기본 설정
st.set_page_config(page_title="탐구비서", page_icon="🚀", layout="wide")

# 요청하신 대로 제목을 '탐구비서'로 복구!
st.title("🚀 탐구비서")
st.markdown("---")

# 2. 사이드바 설정 (비밀 창고 자동 연결)
if 'model' not in st.session_state:
    st.session_state.model = None

with st.sidebar:
    st.header("🔑 AI 엔진 상태")
    try:
        # 스트림릿 비밀 창고(Secrets) 확인
        if "GOOGLE_API_KEY" in st.secrets:
            api_key = st.secrets["GOOGLE_API_KEY"]
            genai.configure(api_key=api_key)
            
            # 엔진 이름 찾기
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            target_model = next((m for m in models if 'flash' in m), models[0])
            
            # [🔥 에러 철벽 방어!] 구글 검색 도구를 가장 안전한 방식으로 연결해
            try:
                # 2026년형 최신 선언 방식 시도
                st.session_state.model = genai.GenerativeModel(
                    model_name=target_model,
                    tools=['google_search'] 
                )
            except:
                try:
                    # 구형 선언 방식 시도
                    st.session_state.model = genai.GenerativeModel(
                        model_name=target_model,
                        tools=[{"google_search": {}}]
                    )
                except:
                    # 도구 연결 실패 시 일반 AI 모드로라도 켜기!
                    st.session_state.model = genai.GenerativeModel(model_name=target_model)
            
            st.success("엔진 가동 준비 완료! ✅")
            st.info(f"사용 엔진: {target_model}")
        else:
            st.error("비밀 창고에 열쇠가 없어! 스트림릿 Settings -> Secrets에 GOOGLE_API_KEY를 넣어줘.")
    except Exception as e:
        st.error(f"연결 오류 발생: {e}")

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
            with st.spinner('🚀 AI가 분석 중입니다...'):
                response = st.session_state.model.generate_content(f"'{topic}'에 대한 최신 이슈를 3가지로 정리해줘.")
                st.info(response.text)
        else:
            st.error("먼저 주제를 입력하고 열쇠 설정을 확인해줘!")

# --- Step 2. 뉴스 검색 및 요약 ---
with tab2:
    st.header("📰 Step 2. 실시간 뉴스 검색 및 요약")
    if st.button("최신 실제 기사 가져오기", key="get_real_news"):
        if st.session_state.model and topic:
            with st.spinner('🗞️ 기사를 찾는 중...'):
                prompt = f"'{topic}' 관련 최신 뉴스 기사의 제목, 언론사, 내용을 알려줘."
                response = st.session_state.model.generate_content(prompt)
                st.session_state.news_text = response.text
                st.success("기사를 가져왔어!")
        else:
            st.error("주제를 먼저 입력해줘!")

    current_text = st.session_state.get('news_text', "")
    long_text = st.text_area("기사 전문", value=current_text, height=200)
    
    if st.button("핵심 요약하기", key="btn2"):
        if st.session_state.model and long_text:
            with st.spinner('📝 요약 중...'):
                response = st.session_state.model.generate_content(f"다음 내용을 3줄 요약해줘:\n\n{long_text}")
                st.info(response.text)

# --- Step 3. 가설설정 ---
with tab3:
    st.header("💡 Step 3. 가설설정")
    if st.button("탐구 가설 추천", key="btn3"):
        if st.session_state.model and topic:
            with st.spinner('🤔 가설 설계 중...'):
                response = st.session_state.model.generate_content(f"'{topic}' 주제에 맞는 중학생 수준 가설 3개를 추천해줘.")
                st.info(response.text)

# --- Step 4. 탐구보고서 개요 ---
with tab4:
    st.header("📄 Step 4. 탐구보고서 개요")
    if st.button("개요 생성", key="btn4"):
        if st.session_state.model and topic:
            with st.spinner('✍️ 개요 작성 중...'):
                response = st.session_state.model.generate_content(f"'{topic}' 주제의 보고서 개요(동기/과정/결과)를 짜줘.")
                st.info(response.text)

# --- Step 5. 탐구보고서 완성 ---
with tab5:
    st.header("✨ Step 5. 탐구보고서 완성")
    if st.button("최종 보고서 완성", key="btn5"):
        if st.session_state.model and topic:
            with st.spinner('🎊 보고서와 출처를 정리 중...'):
                prompt = f"'{topic}' 주제로 서술형 보고서를 써주고 마지막에 [참고 문헌 및 출처]를 넣어줘."
                response = st.session_state.model.generate_content(prompt)
                st.success("완성됐어!")
                st.text_area("최종 보고서", response.text, height=400)
                st.download_button("💾 파일 저장", response.text, file_name=f"{topic}_보고서.txt")}_탐구보고서.txt")

