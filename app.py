import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="THMs 관리 대시보드", layout="wide")

# -----------------------------
# 제목
# -----------------------------
st.title("💧 수도권 THMs 수질 관리 대시보드")
st.markdown("2023~2025 수도권 먹는물 THMs 분석 기반 정책 지원 도구")

# -----------------------------
# 사이드바 (필터)
# -----------------------------
st.sidebar.header("📌 필터")

region = st.sidebar.selectbox(
    "지역 선택",
    ["전체", "서울", "경기", "인천"]
)

quarter = st.sidebar.selectbox(
    "분기 선택",
    ["전체", "Q1", "Q2", "Q3", "Q4"]
)

# -----------------------------
# 샘플 데이터 (추후 CSV 연결)
# -----------------------------
@st.cache_data
def load_data():
    np.random.seed(42)

    months = list(range(1, 13))
    regions = ["서울", "경기", "인천"]

    data = []

    for r in regions:
        for m in months:
            base = np.random.uniform(1, 3)

            # 계절성 반영 (여름 증가)
            if m in [6, 7, 8]:
                base += np.random.uniform(2, 4)

            # 지역 특성 (경기 높음)
            if r == "경기":
                base += 1

            data.append({
                "지역": r,
                "월": m,
                "THMs": round(base, 2),
                "분기": f"Q{(m-1)//3 + 1}"
            })

    return pd.DataFrame(data)

df = load_data()

# -----------------------------
# 필터 적용
# -----------------------------
filtered_df = df.copy()

if region != "전체":
    filtered_df = filtered_df[filtered_df["지역"] == region]

if quarter != "전체":
    filtered_df = filtered_df[filtered_df["분기"] == quarter]

# -----------------------------
# KPI 영역
# -----------------------------
st.subheader("📊 주요 지표")

col1, col2, col3 = st.columns(3)

col1.metric("평균 THMs", round(filtered_df["THMs"].mean(), 2))
col2.metric("최대 THMs", round(filtered_df["THMs"].max(), 2))
col3.metric("최소 THMs", round(filtered_df["THMs"].min(), 2))

# -----------------------------
# 월별 추이
# -----------------------------
st.subheader("📈 월별 THMs 추이")

st.line_chart(filtered_df.groupby("월")["THMs"].mean())

# -----------------------------
# 지역 비교
# -----------------------------
st.subheader("🌍 지역별 비교")

st.bar_chart(filtered_df.groupby("지역")["THMs"].mean())

# -----------------------------
# 정책 인사이트
# -----------------------------
st.subheader("🧠 정책 인사이트")

if quarter == "Q2":
    st.warning("⚠️ 2분기: THMs 증가 시작 → 선제 대응 필요")

elif quarter == "Q3":
    st.error("🚨 3분기: THMs 최고 위험 구간 → 집중 관리 필요")

else:
    st.success("✅ 안정 구간")

# -----------------------------
# 추천 정책
# -----------------------------
st.subheader("📌 정책 제안")

if region == "경기":
    st.markdown("- 경기 지역: **우선 집중 관리 필요**")

st.markdown("""
- 2분기: 염소 주입량 조절 + 모니터링 강화  
- 3분기: 고도처리 + 실시간 관리  
- 관망 개선: 체류시간 감소 및 노후 배관 개선  
- 데이터 기반 예측 시스템 구축  
""")

# -----------------------------
# 원본 데이터
# -----------------------------
with st.expander("📂 데이터 보기"):
    st.dataframe(filtered_df)
