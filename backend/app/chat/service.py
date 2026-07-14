from sqlalchemy.orm import Session

from app.ai.manager import ai_manager
from app.chat.prompt_builder import build_prompt
from app.chat.schemas import ChatRequest
from app.chat.title_generator import generate_title
from app.conversations.message_service import MessageService
from app.conversations.schemas import (
    ConversationCreate,
    MessageCreate,
)
from app.conversations.service import ConversationService
from app.memory.deduplication import is_duplicate_memory
from app.memory.extractor import extract_memory
from app.memory.schemas import MemoryCreate
from app.memory.search import search_memories
from app.memory.service import save_memory


def process_chat(
    db: Session,
    request: ChatRequest,
    user_id: int,
) -> tuple[str, int]:
    """
    Main chat pipeline.
    """

    print("\n========== CHAT PIPELINE ==========")

    # ----------------------------------
    # Conversation
    # ----------------------------------

    conversation_id = request.conversation_id

    if conversation_id is None:

        print("Generating conversation title...")

        title = generate_title(
            request.message
        )

        print(f"Generated Title: {title}")

        conversation = ConversationService.create_conversation(
            db=db,
            user_id=user_id,
            data=ConversationCreate(
                title=title,
            ),
        )

        conversation_id = conversation.id

        print(f"Created Conversation: {conversation_id}")

    else:

        print(f"Using Conversation: {conversation_id}")

    # ----------------------------------
    # Save user message
    # ----------------------------------

    MessageService.create_message(
        db=db,
        conversation_id=conversation_id,
        data=MessageCreate(
            role="user",
            content=request.message,
        ),
    )

    # ----------------------------------
    # Memory Extraction
    # ----------------------------------

    extracted_memory = extract_memory(
        request.message
    )

    if extracted_memory:

        duplicate = is_duplicate_memory(
            memory=extracted_memory,
            user_id=user_id,
        )

        if not duplicate:

            save_memory(
                db=db,
                user_id=user_id,
                memory=MemoryCreate(
                    content=extracted_memory,
                ),
            )

    # ----------------------------------
    # Long-Term Memory
    # ----------------------------------

    memories = search_memories(
        query=request.message,
        user_id=user_id,
        limit=5,
    )

    if memories:

        memory_context = "\n".join(
            f"- {memory['content']}"
            for memory in memories
        )

    else:

        memory_context = "No relevant memories."

    # ----------------------------------
    # Conversation History
    # ----------------------------------

    history = MessageService.list_messages(
        db=db,
        conversation_id=conversation_id,
    )

    # ----------------------------------
    # Prompt Builder
    # ----------------------------------

    prompt = build_prompt(
        conversation_messages=history.messages,
        memory_context=memory_context,
        current_message=request.message,
    )

    print("Sending prompt to Gemini...")

    response = ai_manager.chat(
        prompt
    )

    # ----------------------------------
    # Save assistant response
    # ----------------------------------

    MessageService.create_message(
        db=db,
        conversation_id=conversation_id,
        data=MessageCreate(
            role="assistant",
            content=response,
        ),
    )

    print("========== DONE ==========\n")

    return response, conversation_id