import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import streamlit as st
import plotly.express as px
import pdfplumber

from recommendation import recommend_top_skills, recommend_skills_for_role, match_role
from skill_analysis import get_top_skills, get_all_roles
from preprocess import get_processed_data
from skill_cluster import cluster_skills
from resume_parser import extract_skills_from_text
from nlp_engine import get_similarity_scores
from bert_engine import bert_similarity
from career_path import get_career_path
from matcher import calculate_match
from chatbot import career_chatbot
from user_profile import save_profile, load_profile
from report_generator import generate_report

# ------------------ CONFIG ------------------
st.set_page_config(
    page_title="AI Job Market Intelligence",
    layout="wide"
)

# ------------------ STYLE ------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
h1, h2, h3 {
    letter-spacing: -0.5px;
}
.metric-label {
    font-size: 14px;
    color: #aaa;
}
.metric-value {
    font-size: 28px;
    font-weight: bold;
}
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

def render_skill_chips(skills):
    cols = st.columns(4)  
    for i, skill in enumerate(skills):
        cols[i % 4].markdown(
            f"<div style='padding:8px 12px; margin:5px; background:#0e1a2b; border-radius:10px; text-align:center;'>• {skill}</div>",
            unsafe_allow_html=True
        )

# ------------------ HEADER ------------------
st.markdown("""
<h1 style='font-size:48px;'>🚀 AI Job Market Intelligence</h1>
<p style='color:gray; font-size:18px'>
Analyze trends, discover in-demand skills, and close your career gap
</p>
""", unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------
st.sidebar.header("⚙️ Select Options")

roles = get_all_roles()
search_input = st.sidebar.text_input("🔍 Search Role")
filtered_roles = [r for r in roles if search_input.lower() in r.lower()]
use_ai = st.sidebar.toggle("Use Advanced AI (BERT)", value=False)

if filtered_roles:
    role = st.sidebar.selectbox("Select Matching Role", filtered_roles)
else:
    role = "data scientist"

# NLP Matching
if search_input:
    if use_ai:
        scores = bert_similarity(search_input, roles)
        st.sidebar.write("🧠 Using AI")
    else:
        scores = get_similarity_scores(search_input, roles)
        st.sidebar.write("⚡ Fast Mode")

    best_match = roles[scores.argmax()]
    st.sidebar.write(f"🎯 Best Match: {best_match}")

num_skills = st.sidebar.slider("Number of skills", 5, 20, 10)

# ------------------ DATA ------------------
top_data = get_top_skills(num_skills)
skills = [skill for skill, count in top_data]
counts = [count for skill, count in top_data]
role_skills = recommend_skills_for_role(role, num_skills)

# ------------------ KPI CARDS ------------------
st.markdown("## 📊 Market Overview")
col1, col2, col3 = st.columns(3)

col1.markdown(f"""
<div class="card">
<div class="metric-label">🔥 Top Skill</div>
<div class="metric-value">{skills[0]}</div>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div class="card">
<div class="metric-label">📈 Skills Analyzed</div>
<div class="metric-value">{len(skills)}</div>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div class="card">
<div class="metric-label">💼 Role</div>
<div class="metric-value">{role.title()}</div>
</div>
""", unsafe_allow_html=True)

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
render_skill_chips(role_skills)

# ------------------ SKILL GAP ------------------
st.markdown("## 🧠 Skill Gap Analysis")

user_skills = st.text_input("Enter your skills (comma separated)")

if user_skills:
    user_skills = [s.strip().lower() for s in user_skills.split(",")]
    gap = [skill for skill in role_skills if skill not in user_skills]

    if gap:
        st.success("🚀 Skills you should focus on:")
        render_skill_chips(gap)
    else:
        st.success("🔥 You already have the top skills!")

# -----------Extract Skills from resume -----------
st.markdown("## 📄 Resume Skill Extraction")
uploaded_file = st.file_uploader("Upload your resume (TXT only for now)")

content = None
extracted = []

if uploaded_file:
    try:
        if uploaded_file.type == "application/pdf":
            with pdfplumber.open(uploaded_file) as pdf:
                content = ""
                for page in pdf.pages:
                    content += page.extract_text() or ""
        else:
            content = uploaded_file.read().decode("utf-8", errors="ignore")

        all_skills = [s for s, _ in get_top_skills(100)]
        extracted = extract_skills_from_text(content, all_skills)

        st.success("✅ Extracted Skills")
        render_skill_chips(extracted)

    except:
        st.error("Error reading file")

st.markdown("## 🎯 Resume vs Job Match")
job_desc = st.text_area("Paste Job Description")

if content and job_desc:
    try:
        content = uploaded_file.read().decode("utf-8", errors="ignore")
        score = calculate_match(content, job_desc)
        st.metric("📊 Match Score", f"{score}%")

        if score > 70:
            st.success("🔥 Strong Match!")
        elif score > 40:
            st.warning("⚡ متوسط match — improve skills")
        else:
            st.error("❌ Low match — upskill needed")

    except:
        st.error("Error processing files")

# ------------------ AI INSIGHT ------------------
st.markdown("## 🤖 AI Insight")

if len(role_skills) >= 3:
    st.info(f"""
For the role **{role.title()}**, the market strongly emphasizes:

👉 **{role_skills[0]}**, **{role_skills[1]}**, and **{role_skills[2]}**

Focus on mastering these to significantly improve your career opportunities.
""")
# ------------------ CAREER PATH ------------------
st.markdown("## 🚀 Career Path")
next_roles = get_career_path(role)

if next_roles:
    for r in next_roles:
        st.markdown(f"➡️ {r}")
else:
    st.info("No predefined career path for this role yet.")

# ------------------ SKILL CLUSTERS ------------------
cluster_labels = {
    0: "💻 Programming & Development",
    1: "📊 Management & Governance",
    2: "⚙️ Data Engineering & Pipelines",
    3: "📈 Reporting & Analytics",
    4: "🤖 Machine Learning & AI"
}
st.markdown("## 🧠 AI Skill Intelligence Clusters")
clusters = cluster_skills(5)

for cluster_id, skills_list in clusters.items():
    label = cluster_labels.get(cluster_id, f"Cluster {cluster_id}")

    with st.expander(label):
        render_skill_chips(skills_list[:12])

st.markdown("## 🤖 Career Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_q = st.text_input("Ask anything about your career")

if user_q:
    response = career_chatbot(user_q, role, st.session_state.chat_history)

    st.session_state.chat_history.append(("user", user_q))
    st.session_state.chat_history.append(("bot", response))

for sender, msg in st.session_state.chat_history[-6:]:
    if sender == "user":
        st.markdown(f"**🧑 You:** {msg}")
    else:
        st.markdown(f"**🤖 AI:** {msg}")

# ------------------ SAVE PROFILE ------------------
st.markdown("## 👤 Save Your Profile")
name = st.text_input("Your Name")

if st.button("Save Profile"):
    if uploaded_file:
        save_profile(name, extracted if 'extracted' in locals() else [])
    else:
        save_profile(name, [])

    st.success("✅ Profile Saved")

from user_profile import load_profile

if name:
    profile = load_profile(name)
    if profile:
        st.markdown("### 📂 Saved Profile")
        render_skill_chips(profile)

st.markdown("## 📥 Download Career Report")

if st.button("Generate Report"):
    report_file = generate_report(
        name if name else "User",
        role,
        role_skills,
        gap if 'gap' in locals() else [],
        score if 'score' in locals() else 0
    )

    with open(report_file, "rb") as f:
        st.download_button(
            label="📄 Download PDF",
            data=f,
            file_name="career_report.pdf",
            mime="application/pdf"
        )