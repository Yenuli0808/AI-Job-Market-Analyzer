import json
import os
from datetime import datetime

PROFILES_DIR = "profiles"
os.makedirs(PROFILES_DIR, exist_ok=True)

def _profile_path(name: str) -> str:
    safe = name.strip().lower().replace(" ", "_") or "default"
    return os.path.join(PROFILES_DIR, f"{safe}.json")

def save_profile(name: str, skills: list, role: str = "") -> None:
    data = {
        "name": name,
        "skills": skills,
        "role": role,
        "saved_at": datetime.now().isoformat(),
    }
    try:
        with open(_profile_path(name), "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving profile: {e}")

def load_profile(name: str = "") -> dict:
    try:
        with open(_profile_path(name), "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"Error loading profile: {e}")
        return {}