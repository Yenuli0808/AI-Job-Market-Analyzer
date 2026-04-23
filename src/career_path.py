def get_career_path(role: str) -> list:
    role = role.lower().strip()

    paths = {
        "data analyst":         ["senior data analyst", "data scientist", "business intelligence engineer"],
        "data scientist":       ["senior data scientist", "ml engineer", "ai engineer"],
        "senior data scientist":["principal data scientist", "head of data", "ai architect"],
        "data engineer":        ["senior data engineer", "analytics engineer", "mlops engineer"],
        "senior data engineer": ["data architect", "platform engineer", "head of data engineering"],
        "ml engineer":          ["senior ml engineer", "ai engineer", "mlops engineer"],
        "senior ml engineer":   ["principal ml engineer", "ai architect", "head of ml"],
        "mlops engineer":       ["senior mlops engineer", "platform engineer", "ai infrastructure lead"],
        "software engineer":    ["senior software engineer", "tech lead", "solutions architect"],
        "ai engineer":          ["senior ai engineer", "ai architect", "head of ai"],
        "business analyst":     ["senior business analyst", "data analyst", "product manager"],
    }

    # Fuzzy key match
    for key, value in paths.items():
        if key in role or role in key:
            return value

    return ["data scientist", "ml engineer", "ai engineer"]