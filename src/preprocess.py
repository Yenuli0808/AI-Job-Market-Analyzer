import pandas as pd

# Load data
def load_data():
    jobs = pd.read_csv("DataSet/DataScience_Job_Postings_&_Skills-DataSet/job_postings.csv")
    skills = pd.read_csv("DataSet/DataScience_Job_Postings_&_Skills-DataSet/job_skills.csv")

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
        "sql databases": "sql"
    }

    df["job_skills"] = df["job_skills"].apply(lambda x: skill_map.get(x, x))

    # Remove empty values
    df = df[df["job_skills"] != ""]
    df = df.dropna(subset=["job_skills"])

    return df

# Full pipeline
def get_processed_data():

    df = load_data()
    df = clean_data(df)
    df = process_skills(df)

    return df