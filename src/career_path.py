def get_career_path(role):
    role = role.lower()
    paths = {
        "data analyst": ["data scientist", "ml engineer", "senior data analyst"],
        "data scientist": ["senior data scientist", "ai engineer","ml engineer"],
        "data engineer": ["senior data engineer", "ml engineer", "mlops engineer"],
        "ml engineer": ["senior ml engineer", "ai architect"],
        "mlops engineer": ["ai engineer", "platform engineer"],
        "software engineer": ["senior software engineer", "tech lead"]
    }
    for key in paths:
        if key in role:
            return paths[key]

    return ["data scientist", "data engineer", "ml engineer"]