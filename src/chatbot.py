import requests
import json

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
# Set your API key in your environment: export ANTHROPIC_API_KEY="sk-..."
import os
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

def chatbot_response(user_q: str, role: str, history: list = None) -> str:
    """
    Calls Claude API for real conversational responses.
    history: list of ("user"|"bot", message) tuples from st.session_state
    """
    if not API_KEY:
        return "⚠️ ANTHROPIC_API_KEY not set. Add it to your environment variables."

    # Build message history for Claude
    messages = []
    if history:
        for sender, msg in history[:-2]:  # exclude the current question
            role_name = "user" if sender == "user" else "assistant"
            messages.append({"role": role_name, "content": msg})

    # Add current user message
    messages.append({"role": "user", "content": user_q})

    system_prompt = f"""You are an expert AI career advisor specializing in data science, 
machine learning, and data engineering roles. The user is currently exploring or targeting 
the role of **{role}**.

Your job:
- Give specific, actionable advice about skills, learning paths, salary, tools, and career progression
- Reference real tools, frameworks, and industry standards
- Be concise but complete — 3-5 sentences per response unless the user asks for more
- If the user says "yes" or "show me" as a follow-up, expand on what you just said
- Never give generic filler responses

Current target role: {role}"""

    try:
        response = requests.post(
            ANTHROPIC_API_URL,
            headers={
                "x-api-key": API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-haiku-4-5-20251001",  # fast + cheap for chat
                "max_tokens": 400,
                "system": system_prompt,
                "messages": messages,
            },
            timeout=15,
        )
        data = response.json()
        if "content" in data and data["content"]:
            return data["content"][0]["text"]
        elif "error" in data:
            return f"API error: {data['error'].get('message', 'Unknown error')}"
        else:
            return "I couldn't generate a response. Please try again."
    except requests.Timeout:
        return "⏱️ Response timed out. Please try again."
    except Exception as e:
        return f"Error connecting to AI: {str(e)}"