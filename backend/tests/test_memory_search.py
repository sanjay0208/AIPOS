from app.memory.search import search_memories


def main():
    query = "What programming language do I like?"

    print(f"\nQuery: {query}\n")

    memories = search_memories(
        query=query,
        limit=5,
    )

    if not memories:
        print("No memories found.")
        return

    print("Retrieved Memories:\n")

    for index, memory in enumerate(memories, start=1):
        print(f"{index}. {memory['content']}")


if __name__ == "__main__":
    main()