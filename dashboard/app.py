import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import streamlit as st
from recommendation import recommend_top_skills, recommend_skills_for_role
import plotly.express as px
from skill_analysis import get_top_skills

st.set_page_config(page_title="AI Job Market Intelligence System", layout="wide")
st.title("🚀 AI Job Market Intelligence System")
st.write("Analyze job market trends and get skill recommendations")
st.markdown("""
<style>
.big-title {
    font-size: 40px;
    font-weight: bold;
}
.card {
    padding: 20px;
    border-radius: 15px;
    background-color: #111;
}
</style>
""", unsafe_allow_html=True)

# SIDEBAR

st.sidebar.header("Select Options")

role = st.sidebar.selectbox(
    "Choose a Role",
    ["data scientist", "data analyst", "machine learning engineer"]
)

num_skills = st.sidebar.slider("Number of skills", 5, 20, 10)

# GLOBAL SKILLS

st.subheader("🌍 Top Skills in Market")

top_data = get_top_skills(num_skills)

skills = [skill for skill, count in top_data]
counts = [count for skill, count in top_data]

fig = px.bar(
    x=counts,
    y=skills,
    orientation='h',
    title="Top Skills Demand",
)

st.plotly_chart(fig)

# ROLE-BASED SKILLS

st.subheader(f"🎯 Skills for {role.title()}")

role_skills = recommend_skills_for_role(role, num_skills)

for skill in role_skills:
    st.write(f"📌 {skill}")