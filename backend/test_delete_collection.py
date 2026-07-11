from app.vector.client import client

client.delete_collection("memories")

print("Collection deleted.")