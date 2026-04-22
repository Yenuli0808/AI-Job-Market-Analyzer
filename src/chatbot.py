def career_chatbot(user_input, role=None, history=None):
    user_input = user_input.lower()

    if history is None:
        history = []

    # Context awareness
    if "skill" in user_input:
        if role:
            return f"For {role}, focus on Python, SQL, and domain-specific tools."

    if "advanced" in user_input:
        return "Advanced skills include ML, system design, and cloud platforms."

    if "career" in user_input:
        return f"You can grow from {role} → senior → leadership roles."

    # fallback
    return "Try asking about skills, career growth, or job matching."