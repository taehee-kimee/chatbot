import streamlit as st
from openai import OpenAI

# 앱 제목 및 설명
st.title("Sing Sing")
st.write("안녕하세요! 싱가폴 맛집 전문 AI 가이드에요")

# st.secrets에서 API 키 확인
if "OPENAI_API_KEY" in st.secrets:
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    
    # ❗️ 1. 여기서 OpenAI 클라이언트를 생성해야 합니다.
    client = OpenAI(api_key=openai_api_key)

    # 세션 상태에 메시지 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "안녕하세요! 어딜 가실건가요?"}
        ]

    # 기존 대화 내용 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 채팅 입력창
    if prompt := st.chat_input("가고싶은 곳을 입력하세요."):
        # 사용자 메시지 추가 및 표시
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # ❗️ 2. API에 보낼 메시지 목록을 올바르게 구성합니다.
        # 시스템 메시지 + 전체 대화 기록
        messages_to_send = [
            {"role": "system", "content": "너는 싱가폴 가족여행 전문 맛집가이드야. number bullet point를 사용해서 항상 우선순위를 기반으로 대답해줘. 순위는 google 맵 맛집 별점을 기반으로. 모든 답변은 한국어로. 대상 사용자는 16개월 아기와 동행하는 가족이야."}
        ]
        for m in st.session_state.messages:
            messages_to_send.append({"role": m["role"], "content": m["content"]})
        
        # OpenAI API를 통해 응답 생성
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages_to_send, # 수정된 메시지 목록 사용
            stream=True,
        )

        # 스트리밍 응답 표시 및 저장
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

else:
    # API 키가 secrets.toml에 없을 경우 안내 메시지 표시
    st.error("OpenAI API 키를 .streamlit/secrets.toml 파일에 설정해주세요.")
