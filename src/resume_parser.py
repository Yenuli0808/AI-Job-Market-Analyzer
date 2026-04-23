import re

SKILL_ALIASES = {
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "nlp": "natural language processing",
    "dl": "deep learning",
}

def extract_skills_from_text(text: str, skills_list: list) -> list:
    text = text.lower()
    # Normalize aliases
    for alias, full in SKILL_ALIASES.items():
        text = re.sub(rf'\b{re.escape(alias)}\b', full, text)

    found = []
    for skill in skills_list:
        # Use word boundary to avoid "r" matching inside "programming"
        pattern = rf'\b{re.escape(skill.lower())}\b'
        if re.search(pattern, text):
            found.append(skill)

    return list(set(found))