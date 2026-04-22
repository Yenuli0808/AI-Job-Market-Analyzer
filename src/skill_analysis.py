from collections import Counter
from preprocess import get_processed_data

# Get top skills from the processed data
def get_top_skills(n=10):
    df = get_processed_data()
    skill_counts = Counter(df["job_skills"])
    return skill_counts.most_common(n)

# skills by role
def get_skills_by_role(role, top_n=10):
    df = get_processed_data()

    # Filter by role
    df_role = df[df["job_title"].str.contains(role.lower(), na=False)]
    skill_counts = Counter(df_role["job_skills"])
    return skill_counts.most_common(top_n)

# Total Unique skills across all job postings
def get_total_unique_skills():
    df = get_processed_data()
    return df["job_skills"].nunique()

def get_all_roles(top_n=20):
    df = get_processed_data()
    return df["job_title"].value_counts().head(top_n).index.tolist()

# Main test
if __name__ == "__main__":

    print("\n🔥 Top Skills Overall:\n")
    for skill, count in get_top_skills(10):
        print(f"{skill}: {count}")

    print("\n📊 Skills for Data Scientist:\n")
    for skill, count in get_skills_by_role("data scientist", 10):
        print(f"{skill}: {count}")

    print("\n📌 Total Unique Skills:", get_total_unique_skills())