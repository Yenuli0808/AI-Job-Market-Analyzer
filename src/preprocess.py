import streamlit as st
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_data():
    jobs = pd.read_csv(os.path.join(BASE_DIR, "DataSet/DataScience_Job_Postings_&_Skills/job_postings.csv"))
    skills = pd.read_csv(os.path.join(BASE_DIR, "DataSet/DataScience_Job_Postings_&_Skills/job_skills.csv"))
    return jobs.merge(skills, on="job_link")

def clean_data(df):
    df = df.drop_duplicates().dropna(subset=["job_skills"])
    df["job_title"] = df["job_title"].str.lower()
    df["job_skills"] = df["job_skills"].str.lower()
    return df

def process_skills(df):
    skill_map = {
        "ml": "machine learning", "ai": "artificial intelligence",
        "python programming": "python", "sql databases": "sql",
        "communication skills": "communication", "data analytics": "data analysis",
        "visualization": "data visualization", "dl": "deep learning",
        "nlp": "natural language processing", "cv": "computer vision",
        "js": "javascript", "ts": "typescript", "k8s": "kubernetes",
        "devops": "dev ops", "bi": "business intelligence",
    }
    df["job_skills"] = df["job_skills"].apply(lambda x: x.split(","))
    df["job_skills"] = df["job_skills"].apply(lambda s: [i.strip() for i in s])
    df = df.explode("job_skills")
    df["job_skills"] = df["job_skills"].apply(lambda x: skill_map.get(x, x))
    df = df[df["job_skills"].str.strip() != ""].dropna(subset=["job_skills"])
    return df

# Massively expanded category map — this is the core fix for Issue 1
CATEGORY_MAP = {
    "Programming": [
        "python", "java", "scala", "r", "c++", "c#", "go", "rust", "julia",
        "javascript", "typescript", "php", "ruby", "swift", "kotlin", "matlab",
        "bash", "shell", "perl", "groovy", "javafx", "oop", "object oriented",
    ],
    "Tools & Platforms": [
        "excel", "power bi", "tableau", "looker", "qlik", "sas", "spss",
        "jupyter", "git", "github", "gitlab", "docker", "kubernetes", "airflow",
        "dbt", "jenkins", "terraform", "figma", "jira", "confluence", "linux",
        "unix", "windows server", "databricks", "snowflake", "dask",
    ],
    "Soft Skills": [
        "communication", "leadership", "teamwork", "collaboration", "presentation",
        "problem solving", "analytical thinking", "adaptability", "time management",
        "critical thinking", "attention to detail", "project management",
        "stakeholder management", "decision making", "mentoring",
    ],
    "AI/ML": [
        "machine learning", "deep learning", "natural language processing",
        "computer vision", "artificial intelligence", "tensorflow", "keras",
        "pytorch", "scikit-learn", "xgboost", "lightgbm", "hugging face",
        "transformers", "reinforcement learning", "neural networks", "mlops",
        "feature engineering", "model deployment", "llm", "generative ai",
        "nlp", "bert", "gpt", "regression", "classification", "clustering",
    ],
    "Data Engineering": [
        "data engineering", "etl", "data warehouse", "data warehousing",
        "kafka", "spark", "hadoop", "flink", "hive", "presto", "trino",
        "data pipeline", "data lake", "data lakehouse", "aws glue", "nifi",
        "data ingestion", "data validation", "data transformation",
        "batch processing", "stream processing", "data architecture",
        "data modeling", "data quality", "data governance",
    ],
    "Cloud & Databases": [
        "aws", "azure", "gcp", "google cloud", "amazon web services",
        "cloud computing", "s3", "ec2", "redshift", "bigquery",
        "sql", "mysql", "postgresql", "mongodb", "cassandra", "redis",
        "dynamodb", "oracle", "sql server", "nosql", "database",
        "data analysis", "data science", "statistics", "mathematics",
        "analytics", "reporting", "business intelligence", "data visualization",
        "pandas", "numpy", "scipy", "r programming", "excel analysis",
    ],
}

def categorize_skill(skill):
    skill = skill.lower().strip()
    for category, keywords in CATEGORY_MAP.items():
        for kw in keywords:
            if kw in skill or skill in kw:
                return category
    return "Other"

@st.cache_data
def get_processed_data():
    df = load_data()
    df = clean_data(df)
    df = process_skills(df)
    df["category"] = df["job_skills"].apply(categorize_skill)
    return df