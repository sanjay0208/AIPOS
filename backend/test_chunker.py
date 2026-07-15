from app.knowledge.chunker import DocumentChunker

text = "Python " * 500

chunks = DocumentChunker.split(text)

print()

print("Chunks:", len(chunks))

for i, chunk in enumerate(chunks):

    print(
        f"Chunk {i+1}:",
        len(chunk),
        "characters",
    )