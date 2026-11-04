import requests
import chromadb
import uuid

from pathlib import Path


# ==========================================
# CONFIGURATION
# ==========================================

OLLAMA_URL = "http://localhost:11434/api/embed"

EMBEDDING_MODEL = "nomic-embed-text"

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DB_PATH = PROJECT_ROOT / "data" / "chroma_db"


# ==========================================
# VECTOR DATABASE CLASS
# ==========================================

class VectorDatabase:

    def __init__(self):

        # Create persistent ChromaDB client
        self.client = chromadb.PersistentClient(
            path=str(DB_PATH)
        )

        # Create or access collection
        self.collection = self.client.get_or_create_collection(
            name="nova_knowledge",
            metadata={"hnsw:space": "cosine"}
        )

        print("NOVA Vector Database initialized!")

    # ======================================
    # GENERATE EMBEDDINGS
    # ======================================

    def generate_embeddings(self, texts):

        if isinstance(texts, str):
            texts = [texts]

        if not texts:
            return []

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": EMBEDDING_MODEL,
                "input": texts
            },
            timeout=120
        )

        response.raise_for_status()

        embeddings = response.json()["embeddings"]

        return embeddings

    # ======================================
    # ADD DOCUMENTS
    # ======================================

    def add_documents(self, chunks, metadata):

        if not chunks:
            raise ValueError("No document chunks provided.")

        if len(chunks) != len(metadata):
            raise ValueError(
                "Chunks and metadata counts do not match."
            )

        total_added = 0

        # Process in batches
        batch_size = 32

        for start in range(0, len(chunks), batch_size):

            batch_chunks = chunks[start:start + batch_size]

            batch_metadata = metadata[start:start + batch_size]

            embeddings = self.generate_embeddings(
                batch_chunks
            )

            ids = [
                str(uuid.uuid4())
                for _ in batch_chunks
            ]

            self.collection.add(
                ids=ids,
                documents=batch_chunks,
                embeddings=embeddings,
                metadatas=batch_metadata
            )

            total_added += len(batch_chunks)

        print(f"Successfully stored {total_added} chunks!")

        return total_added

    # ======================================
    # SEARCH DOCUMENTS
    # ======================================

    def search(self, query, top_k=5):

        if not query.strip():
            return []

        total_documents = self.collection.count()

        if total_documents == 0:
            return []

        query_embedding = self.generate_embeddings(
            query
        )[0]

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, total_documents),
            include=[
                "documents",
                "metadatas",
                "distances"
            ]
        )

        search_results = []

        for i in range(len(results["documents"][0])):

            search_results.append({

                "text": results["documents"][0][i],

                "metadata": results["metadatas"][0][i],

                "distance": results["distances"][0][i]

            })

        return search_results

    # ======================================
    # DATABASE STATISTICS
    # ======================================

    def get_database_count(self):

        return self.collection.count()


# ==========================================
# CREATE DATABASE INSTANCE
# ==========================================

if __name__ == "__main__":

    db = VectorDatabase()

    print(
        "Total stored documents:",
        db.get_database_count()
    )