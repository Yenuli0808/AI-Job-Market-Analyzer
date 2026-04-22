from skill_analysis import get_top_skills, get_skills_by_role
from difflib import get_close_matches

# Global Recommendation
def recommend_top_skills(n=10):
    top_skills = get_top_skills(n)
    return [skill for skill, count in top_skills]

# Role-based Recommendation
def recommend_skills_for_role(role, n=10):
    role_skills = get_skills_by_role(role, n)
    return [skill for skill, count in role_skills]

def match_role(user_input, roles):
    matches = get_close_matches(user_input, roles, n=1, cutoff=0.3)
    return matches[0] if matches else user_input

# Smart recommendation
def recommend_combined(role, n=10):
    global_skills = recommend_top_skills(n)
    role_skills = recommend_skills_for_role(role, n)

    # combine + remove duplicates while preserving order
    combined = list(dict.fromkeys(role_skills + global_skills))
    return combined[:n]

# Main Test
if __name__ == "__main__":
    print("\n🌍 Top Skills to Learn:\n")
    for skill in recommend_top_skills(10):
        print(f"- {skill}")

    print("\n🎯 Skills for Data Scientist:\n")
    for skill in recommend_skills_for_role("data scientist", 10):
        print(f"- {skill}")

    print("\n🚀 Smart Combined Recommendation:\n")
    for skill in recommend_combined("data scientist", 10):
        print(f"- {skill}")