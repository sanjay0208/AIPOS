from app.vector.client import client

print("Connected!")

collections = client.get_collections()

print(collections)