import os
from datetime import datetime, timedelta
import streamlit as st
from openai import OpenAI

# --- API 키 설정 ---
os.environ["OPENAI_API_KEY"] = st.secrets["API_KEY"]
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# --- 앱 제목 ---
st.title("시험 공부 계획 자동 생성 앱 📝")

# --- 사용자 입력 ---
st.header("시험 정보 입력")
num_subjects = st.number_input("시험 과목 수", min_value=1, step=1)

subjects = []
for i in range(num_subjects):
    st.subheader(f"과목 {i+1}")
    name = st.text_input(f"과목명", key=f"name_{i}")
    exam_date = st.date_input(f"시험 날짜", key=f"date_{i}")
    scope = st.text_area(f"공부 범위", key=f"scope_{i}")
    if name and exam_date and scope:
        subjects.append({"name": name, "date": exam_date, "scope": scope})

# --- 버튼 클릭 시 계획 생성 ---
if st.button("공부 계획 생성"):
    if not subjects:
        st.warning("과목 정보를 모두 입력해주세요!")
    else:
        st.success("AI가 공부 계획을 생성 중입니다... ⏳")
        
        # 각 과목별로 AI에게 하루 단위 계획 요청
        for subj in subjects:
            days_left = (subj["date"] - datetime.today().date()).days + 1
            prompt = f"""
            나는 학생입니다. 남은 시험 기간 {days_left}일 동안
            '{subj['name']}' 과목을 공부해야 합니다.
            공부 범위는 다음과 같습니다: {subj['scope']}
            
            AI에게 하루 단위 학습 계획을 생성해달라고 요청합니다.
            하루 공부량과 순서를 추천해주고, 
            각 날마다 구체적인 공부 목표를 제시해주세요.
            결과를 마크다운 형식으로 1일차, 2일차 ... 로 나눠서 만들어주세요.
            """
            
            chat_completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "당신은 친절한 학습 코치입니다."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            plan = chat_completion.choices[0].message.content
            st.markdown(f"### 📘 {subj['name']} 공부 계획")
            st.markdown(plan)
