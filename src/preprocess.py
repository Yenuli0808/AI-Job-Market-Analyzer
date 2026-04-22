import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load data
def load_data():
    jobs = pd.read_csv(os.path.join(BASE_DIR, "DataSet/DataScience_Job_Postings_&_Skills/job_postings.csv"))
    skills = pd.read_csv(os.path.join(BASE_DIR, "DataSet/DataScience_Job_Postings_&_Skills/job_skills.csv"))

    df = jobs.merge(skills, on="job_link")
    return df

# Clean data
def clean_data(df):
    df = df.drop_duplicates()
    df = df.dropna(subset=["job_skills"])

    df["job_title"] = df["job_title"].str.lower()
    df["job_skills"] = df["job_skills"].str.lower()

    return df

# Process Skills
def process_skills(df):
    # Convert string → list
    df["job_skills"] = df["job_skills"].apply(lambda x: x.split(","))

    # Remove spaces
    df["job_skills"] = df["job_skills"].apply(lambda skills: [s.strip() for s in skills])

    # Explode (VERY IMPORTANT)
    df = df.explode("job_skills")

    # Normalize skills
    skill_map = {
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "python programming": "python",
    "sql databases": "sql",
    "communication skills": "communication",
    "data analytics": "data analysis",
    "visualization": "data visualization"
}

    df["job_skills"] = df["job_skills"].apply(lambda x: skill_map.get(x, x))

    # Remove empty values
    df = df[df["job_skills"] != ""]
    df = df.dropna(subset=["job_skills"])

    return df

def categorize_skill(skill):
    programming = ["python", "java", "c++", "r"]
    ml_ai = ["machine learning", "deep learning", "ai"]
    tools = ["sql", "aws", "tableau", "power bi"]
    soft = ["communication", "leadership"]

    if skill in programming:
        return "Programming"
    elif skill in ml_ai:
        return "AI/ML"
    elif skill in tools:
        return "Tools"
    elif skill in soft:
        return "Soft Skills"
    else:
        return "Other"

# Full pipeline
def get_processed_data():

    df = load_data()
    df = clean_data(df)
    df = process_skills(df)
    df["category"] = df["job_skills"].apply(categorize_skill)

    return df