import re

# Aliases: what appears in a CV → canonical skill name in our dataset
SKILL_ALIASES = {
    "r programming": "r", "r (programming language)": "r",
    "ml": "machine learning", "ai": "artificial intelligence",
    "nlp": "natural language processing", "dl": "deep learning",
    "oop": "object oriented programming", "ood": "object oriented design",
    "postgresql": "sql", "mysql": "sql", "nosql": "mongodb",
    "scikit-learn": "scikit-learn", "sklearn": "scikit-learn",
    "tensorflow/keras": "tensorflow", "keras": "tensorflow",
    "react.js": "javascript", "flask": "python",
    "boto3": "aws", "sqlalchemy": "sql", "aws s3": "aws", "amazon s3": "aws",
    "amazon ec2": "aws", "gcp": "google cloud",
    "ms excel": "excel", "microsoft excel": "excel",
    "data structures": "data structures and algorithms",
    "hugging face": "hugging face", "javafx": "java",
    "iot": "iot", "figma": "figma",
}

def normalize_text(text: str) -> str:
    text = text.lower()
    for alias, canonical in SKILL_ALIASES.items():
        text = re.sub(rf'\b{re.escape(alias)}\b', canonical, text)
    return text

def extract_skills_from_text(text: str, skills_list: list) -> list:
    normalized = normalize_text(text)
    found = set()

    for skill in skills_list:
        skill_lower = skill.lower().strip()
        if not skill_lower:
            continue
        # Word-boundary match — prevents "r" matching inside "programming"
        # For very short skills (1-2 chars), require surrounding whitespace/punctuation
        if len(skill_lower) <= 2:
            pattern = rf'(?<![a-zA-Z]){re.escape(skill_lower)}(?![a-zA-Z])'
        else:
            pattern = rf'\b{re.escape(skill_lower)}\b'

        if re.search(pattern, normalized):
            found.add(skill)

    # Also do a reverse alias pass: check if any alias maps to a found skill
    for alias, canonical in SKILL_ALIASES.items():
        if re.search(rf'\b{re.escape(alias)}\b', normalized):
            # Find the matching skill in skills_list
            for skill in skills_list:
                if skill.lower() == canonical:
                    found.add(skill)

    return sorted(list(found))