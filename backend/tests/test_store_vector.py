from app.embeddings.service import generate_embedding
from app.vector.service import store_embedding

embedding = generate_embedding(
    "My favorite programming language is Python."
)

vector_id = store_embedding(
    embedding=embedding,
    payload={
        "user_id": 1,
        "content": "My favorite programming language is Python.",
    },
)

print(vector_id)