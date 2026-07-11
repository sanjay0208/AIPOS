from app.memory.extractor import extract_memory

messages = [
    "My favorite programming language is Python.",
    "I live in Chennai.",
    "My goal is to build an AI startup.",
    "Hello, how are you?",
    "What is the weather today?",
]

for message in messages:
    memory = extract_memory(message)

    print("-" * 50)
    print("Message :", message)
    print("Memory  :", memory)