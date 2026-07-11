from app.vector.client import client

points, _ = client.scroll(
    collection_name="memories",
    limit=10,
)

for point in points:
    print(point.id)
    print(point.payload)
    print()