import json

def save_profile(name, skills):
    data = {
        "name": name,
        "skills": skills
    }

    with open("user_profile.json", "w") as f:
        json.dump(data, f)


def load_profile():
    try:
        with open("user_profile.json", "r") as f:
            return json.load(f)
    except:
        return None