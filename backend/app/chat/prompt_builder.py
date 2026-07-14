from app.conversations.schemas import MessageResponse


def build_prompt(
    conversation_messages: list[MessageResponse],
    memory_context: str,
    current_message: str,
) -> str:
    """
    Build the prompt sent to the LLM.
    """

    if conversation_messages:

        conversation_context = "\n".join(
            f"{message.role.capitalize()}: {message.content}"
            for message in conversation_messages[-10:]
        )

    else:

        conversation_context = "No previous conversation."

    prompt = f"""
You are AIPOS, an AI Personal Operating System.

You have access to:

1. Conversation History
2. Long-Term Memory

====================================
Conversation History
====================================

{conversation_context}

====================================
Relevant Long-Term Memory
====================================

{memory_context}

====================================
Current User Message
====================================

{current_message}

Instructions:

- Continue the conversation naturally.
- Prefer recent conversation history.
- Use long-term memories only when relevant.
- Never mention memories explicitly.
"""

    return prompt