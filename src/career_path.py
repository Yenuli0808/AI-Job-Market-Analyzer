def get_career_path(role):
    paths = {
        "data analyst": ["data scientist", "ml engineer"],
        "data scientist": ["senior data scientist", "ai engineer"],
        "data engineer": ["senior data engineer", "ml engineer"]
    }

    return paths.get(role.lower(), [])