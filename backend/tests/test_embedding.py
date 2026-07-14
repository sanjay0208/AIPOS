from app.embeddings.service import generate_embedding

embedding = generate_embedding(
    "My favorite programming language is Python."
)

print(len(embedding))
print(embedding[:5])