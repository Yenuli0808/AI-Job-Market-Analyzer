import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import streamlit as st
import plotly.express as px

from recommendation import recommend_top_skills, recommend_skills_for_role
from skill_analysis import get_top_skills, get_all_roles
from preprocess import get_processed_data

# ------------------ CONFIG ------------------
st.set_page_config(
    page_title="AI Job Market Intelligence",
    layout="wide"
)

# ------------------ STYLE ------------------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}

.card {
    background-color: #111;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
}

.skill-box {
    background-color: #111;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown("""
<h1 style='font-size:48px;'>🚀 AI Job Market Intelligence</h1>
<p style='color:gray; font-size:18px;'>
Analyze trends, discover in-demand skills, and close your career gap
</p>
""", unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------
st.sidebar.header("⚙️ Select Options")

roles = get_all_roles()
role = st.sidebar.selectbox("Choose a Role", roles)

num_skills = st.sidebar.slider("Number of skills", 5, 20, 10)

# ------------------ DATA ------------------
top_data = get_top_skills(num_skills)
skills = [skill for skill, count in top_data]
counts = [count for skill, count in top_data]

role_skills = recommend_skills_for_role(role, num_skills)

# ------------------ KPI CARDS ------------------
st.markdown("## 📊 Market Overview")

col1, col2, col3 = st.columns(3)
col1.metric("🔥 Top Skill", skills[0])
col2.metric("📈 Skills Analyzed", len(skills))
col3.metric("💼 Role", role.title())

# ------------------ CHARTS (SIDE BY SIDE) ------------------
col_left, col_right = st.columns(2)

# BAR CHART
with col_left:
    st.subheader("📊 Top Skills Demand")
    fig = px.bar(
        x=counts,
        y=skills,
        orientation='h',
        color=counts,
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig, use_container_width=True)

# PIE CHART
with col_right:
    st.subheader("📊 Skill Categories")
    df = get_processed_data()

    if "category" in df.columns:
        category_counts = df["category"].value_counts()

        fig2 = px.pie(
            values=category_counts.values,
            names=category_counts.index,
            hole=0.4
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Category data not available")

# ------------------ ROLE SKILLS ------------------
st.markdown(f"## 🎯 Skills for {role.title()}")

for skill in role_skills:
    st.markdown(f"""
    <div class="skill-box">
        🚀 {skill}
    </div>
    """, unsafe_allow_html=True)

# ------------------ SKILL GAP ------------------
st.markdown("## 🧠 Skill Gap Analysis")

user_skills = st.text_input("Enter your skills (comma separated)")

if user_skills:
    user_skills = [s.strip().lower() for s in user_skills.split(",")]

    gap = [skill for skill in role_skills if skill not in user_skills]

    if gap:
        st.success("🚀 Skills you should focus on:")
        for skill in gap:
            st.markdown(f"- {skill}")
    else:
        st.success("🔥 You already have the top skills!")

# ------------------ AI INSIGHT ------------------
st.markdown("## 🤖 AI Insight")

if len(role_skills) >= 3:
    st.info(f"""
For the role **{role.title()}**, the market strongly emphasizes:

👉 **{role_skills[0]}**, **{role_skills[1]}**, and **{role_skills[2]}**

Focus on mastering these to significantly improve your career opportunities.
""")