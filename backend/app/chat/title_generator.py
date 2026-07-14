from app.ai.manager import ai_manager


def generate_title(message: str) -> str:
    """
    Generate a short conversation title from the first message.
    """

    prompt = f"""
Generate a short conversation title.

Rules:

- Maximum 5 words.
- No quotation marks.
- No punctuation at the end.
- Return ONLY the title.
- Make it descriptive.

User Message:

{message}
"""

    title = ai_manager.chat(prompt).strip()

    if len(title) > 60:
        title = title[:60]

    return title