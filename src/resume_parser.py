import re

def extract_skills_from_text(text, skills_list):
    text = text.lower()
    found = []

    for skill in skills_list:
        if skill.lower() in text:
            found.append(skill)

    return list(set(found))