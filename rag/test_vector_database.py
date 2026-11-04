from rag.document_processor import process_pdf

from rag.vector_database import VectorDatabase


print("=" * 50)

print("       NOVA VECTOR DATABASE TEST")

print("=" * 50)


# Initialize database

db = VectorDatabase()


# Process PDF

pdf_path = "data/documents/sample.pdf"

print("\nProcessing PDF...")

chunks, metadata = process_pdf(pdf_path)

print("Total chunks:", len(chunks))


# Store embeddings

print("\nGenerating embeddings...")

db.add_documents(chunks, metadata)


# Display database count

print("\nDatabase Statistics")

print("Stored chunks:", db.get_database_count())


# Test semantic search

print("\nTesting Semantic Search")

question = input("\nAsk something about your PDF: ")

results = db.search(question, top_k=3)


print("\nNOVA SEARCH RESULTS")

for index, result in enumerate(results, start=1):

    print(f"\nResult {index}")

    print("Source:", result["metadata"]["source"])

    print("Page:", result["metadata"]["page"])

    print("Content:", result["text"])

    print("Distance:", result["distance"])


print("\nNOVA VECTOR DATABASE TEST COMPLETED!")