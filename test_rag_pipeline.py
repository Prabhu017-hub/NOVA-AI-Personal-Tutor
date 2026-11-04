from rag.rag_pipeline import RAGPipeline

print("=" * 55)
print("              NOVA RAG AI TUTOR")
print("=" * 55)

try:
    nova = RAGPipeline()

    print("\nNOVA is ready to teach you!")
    print("Ask questions about your uploaded PDF.")
    print("Type 'exit' to stop.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in ["exit", "quit"]:
            print("\nNOVA: Thank you for learning. Goodbye!")
            break

        if not question:
            continue

        print("\nNOVA is thinking...\n")

        try:
            result = nova.ask(question)

            print("NOVA:", result["answer"])

            print("\nSOURCE REFERENCES:")

            if result["sources"]:
                for source in result["sources"]:
                    print(
                        f"Document: {source['source']} | "
                        f"Page: {source['page']}"
                    )
            else:
                print("No relevant source found.")

            print("\n" + "-" * 55)

        except Exception as error:
            print("\nQuestion processing error:", error)

except Exception as error:
    print("\nNOVA initialization failed:", error)