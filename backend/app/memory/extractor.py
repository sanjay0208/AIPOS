from app.ai.manager import ai_manager


def extract_memory(message: str) -> str | None:
    """
    Analyze a user message and determine whether it contains
    long-term personal information worth remembering.

    Returns:
        Extracted memory as a string, or None.
    """

    prompt = f"""
You are an AI memory extraction system.

Your task is to decide whether the user's message contains
long-term personal information that should be remembered.

Examples of information to remember:
- Favorite programming language
- Name
- City
- Occupation
- Preferences
- Goals
- Skills
- Hobbies

Examples NOT to remember:
- Greetings
- Small talk
- Temporary requests
- Questions
- Casual conversation

Rules:
- Return ONLY the memory sentence.
- If nothing should be remembered, return exactly:

NONE

User message:
{message}
"""

    response = ai_manager.chat(prompt).strip()

    if response.upper() == "NONE":
        return None

    return response