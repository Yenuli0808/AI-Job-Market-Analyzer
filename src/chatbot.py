def chatbot_response(user_q, role, history=None):
    user_q_lower = user_q.lower()

    # Support both tuple list [("user", msg)] and dict list [{"user": msg}]
    context = ""
    if history:
        recent = history[-6:]
        for item in recent:
            if isinstance(item, dict):
                context += item.get("user", "") + " "
            elif isinstance(item, tuple) and item[0] == "user":
                context += item[1] + " "

    if any(w in user_q_lower for w in ["skill", "learn", "study"]):
        return f"For **{role}**, focus on Python, SQL, and domain-specific tools. Want me to show the full skill list?"

    elif any(w in user_q_lower for w in ["career", "path", "next", "grow"]):
        return f"From **{role}**, typical progressions are Senior roles, AI Engineer, or specialized tracks like MLOps. Check the Career Path section above."

    elif any(w in user_q_lower for w in ["salary", "pay", "earn", "money"]):
        return f"Salaries for **{role}** vary widely by region. Mid-level roles typically range from $90k–$140k USD in the US. Use LinkedIn Salary or Glassdoor for local figures."

    elif any(w in user_q_lower for w in ["resume", "cv", "upload"]):
        return "Upload your resume in the Resume section above to extract your skills and get a match score against job descriptions."

    elif "previous" in user_q_lower or "before" in user_q_lower:
        return f"You asked earlier about: {context.strip()}" if context else "No previous questions found in this session."

    elif any(w in user_q_lower for w in ["gap", "missing", "need"]):
        return f"Use the Skill Gap Analysis section to see exactly which skills you're missing for **{role}**."

    else:
        return f"I can help with skills, career paths, salary ranges, or resume tips for **{role}**. What would you like to know? 🚀"