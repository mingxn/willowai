import chromadb

# Connect to the ChromaDB server running on localhost:8000
client = chromadb.HttpClient(host="localhost", port=8000)

# List all collections
collections = client.list_collections()

if not collections:
    print("No collections found.")
else:
    print(f"Found {len(collections)} collections.\n")

    for collection in collections:
        print(f"Collection Name: {collection.name}")

        # Get the total count of items in this collection
        count = collection.count()
        print(f"Total items: {count}")

        if count == 0:
            print("No data in this collection.")
        else:
            # Retrieve all data (excluding embeddings for brevity)
            data = collection.get(
                limit=count,
                include=["documents", "metadatas"]
            )

            # Print each item
            for i in range(len(data["ids"])):
                print(f"  ID: {data['ids'][i]}")
                if data["documents"] and data["documents"][i]:
                    print(f"  Document: {data['documents'][i]}")
                if data["metadatas"] and data["metadatas"][i]:
                    print(f"  Metadata: {data['metadatas'][i]}")
                print("  ---")

        print("\n" + "=" * 50 + "\n")