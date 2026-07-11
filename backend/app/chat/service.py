from sqlalchemy.orm import Session

from app.ai.manager import ai_manager
from app.chat.schemas import ChatRequest
from app.memory.deduplication import is_duplicate_memory
from app.memory.extractor import extract_memory
from app.memory.schemas import MemoryCreate
from app.memory.search import search_memories
from app.memory.service import save_memory


def process_chat(
    db: Session,
    request: ChatRequest,
    user_id: int,
) -> str:
    """
    Process a chat request using semantic memory retrieval,
    automatic memory extraction, and duplicate detection.
    """

    print("\n========== MEMORY PIPELINE ==========")
    print("User ID:", user_id)
    print("User Message:", request.message)

    # ----------------------------------
    # Step 1: Extract memory
    # ----------------------------------

    extracted_memory = extract_memory(
        request.message
    )

    print("Extracted Memory:", extracted_memory)

    # ----------------------------------
    # Step 2: Duplicate detection
    # ----------------------------------

    if extracted_memory:

        duplicate = is_duplicate_memory(
            memory=extracted_memory,
            user_id=user_id,
        )

        print("Duplicate:", duplicate)

        if not duplicate:

            print("Saving new memory...")

            save_memory(
                db=db,
                user_id=user_id,
                memory=MemoryCreate(
                    content=extracted_memory,
                ),
            )

        else:

            print("Skipping duplicate memory.")

    else:

        print("No memory extracted.")

    # ----------------------------------
    # Step 3: Retrieve relevant memories
    # ----------------------------------

    memories = search_memories(
        query=request.message,
        user_id=user_id,
        limit=5,
    )

    print(f"Retrieved {len(memories)} relevant memories.")

    if memories:

        memory_context = "\n".join(
            f"- {memory['content']}"
            for memory in memories
        )

    else:

        memory_context = "No relevant memories."

    # ----------------------------------
    # Step 4: Build prompt
    # ----------------------------------

    prompt = f"""
You are AIPOS, a personal AI operating system.

Relevant memories:
{memory_context}

User:
{request.message}

Answer naturally while using the relevant memories whenever appropriate.
"""

    print("Sending prompt to Gemini...")
    print("====================================\n")

    response = ai_manager.chat(prompt)

    return response