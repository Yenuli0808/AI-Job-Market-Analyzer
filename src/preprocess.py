import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load data
def load_data():
    jobs = pd.read_csv(os.path.join(BASE_DIR, "DataSet/DataScience_Job_Postings_&_Skills/job_postings.csv"))
    skills = pd.read_csv(os.path.join(BASE_DIR, "DataSet/DataScience_Job_Postings_&_Skills/job_skills.csv"))
    return jobs.merge(skills, on="job_link")


# Clean data
def clean_data(df):
    df = df.drop_duplicates().dropna(subset=["job_skills"])
    df["job_title"] = df["job_title"].str.lower()
    df["job_skills"] = df["job_skills"].str.lower()
    return df

# Process Skills
def process_skills(df):
    skill_map = {
        "ml": "machine learning", "ai": "artificial intelligence",
        "python programming": "python", "sql databases": "sql",
        "communication skills": "communication", "data analytics": "data analysis",
        "visualization": "data visualization",
    }
    df["job_skills"] = df["job_skills"].apply(lambda x: x.split(","))
    df["job_skills"] = df["job_skills"].apply(lambda s: [i.strip() for i in s])
    df = df.explode("job_skills")
    df["job_skills"] = df["job_skills"].apply(lambda x: skill_map.get(x, x))
    df = df[df["job_skills"].str.strip() != ""].dropna(subset=["job_skills"])
    return df

def categorize_skill(skill):
    skill = skill.lower()

    if skill in ["python", "java", "c++", "r"]:
        return "Programming"
    elif skill in ["sql", "excel", "power bi", "tableau"]:
        return "Tools"
    elif skill in ["communication", "leadership", "teamwork"]:
        return "Soft Skills"
    elif skill in ["machine learning", "deep learning", "nlp"]:
        return "AI/ML"
    elif skill in ["data engineering", "etl", "data warehouse"]:
        return "Data Engineering"
    else:
        return "Other"

# Full pipeline
def get_processed_data():

    df = load_data()
    df = clean_data(df)
    df = process_skills(df)
    df["category"] = df["job_skills"].apply(categorize_skill)

    return df