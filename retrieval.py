from ingest import load_parse_chunks
import chromadb
from sentence_transformers import SentenceTransformer

# Load chunks
chunks = load_parse_chunks("documents")
print("Loaded chunks:", len(chunks))

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# ChromaDB setup
client = chromadb.Client()
collection = client.get_or_create_collection("professor_reviews")

# Store embeddings
for i, chunk in enumerate(chunks):
    text = f"{chunk['professor']} {chunk['review']}"
    embedding = model.encode(text).tolist()

    collection.add(
        ids=[str(i)],
        embeddings=[embedding],
        documents=[chunk["review"]],
        metadatas=[{
            "professor": chunk["professor"],
            "source": chunk["source"]
        }]
    )

print("Stored all embeddings in ChromaDB")


# Search function
def search(query, k=5):
    results = collection.query(
        query_texts=[query],
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )
    return results


# Test multiple queries (Milestone 4 requirement)
def test_search():
    queries = [
        "Which professors are easiest at UW?",
        "Which professors are hardest?",
        "Which professors are most recommended?",
        "Which professors require strict attendance?",
        "Which professors have confusing lectures?"
    ]

    for query in queries:
        print("\n==============================")
        print("QUERY:", query)
        print("==============================")

        results = search(query, k=5)

        for i in range(len(results["documents"][0])):
            print("\n--- Result", i + 1, "---")
            print("Professor:", results["metadatas"][0][i]["professor"])
            print("Source:", results["metadatas"][0][i]["source"])
            print("Review:", results["documents"][0][i])
            print("Distance:", results["distances"][0][i])


if __name__ == "__main__":
    test_search()