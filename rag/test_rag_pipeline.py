from rag.rag_pipeline import RAGPipeline


print("=" * 50)

print("       NOVA RAG PIPELINE TEST")

print("=" * 50)


# Initialize NOVA

nova = RAGPipeline()


print("\nNOVA is ready to teach you!")

print("\nAsk questions about your uploaded PDF.")

print("Type 'exit' to close NOVA.")


while True:

    question = input("\nYou: ").strip()

    if question.lower() in ["exit", "quit"]:

        print("\nNOVA: Thank you! Goodbye!")

        break

    if not question:
        continue

    try:

        result = nova.ask(question)

        print("\n" + "=" * 50)

        print("NOVA RESPONSE")

        print("=" * 50)

        print(result["answer"])

        print("\nSOURCE REFERENCES")

        for source in result["sources"]:

            print(
                f"Document: {source['source']} | "
                f"Page: {source['page']}"
            )

    except Exception as error:

        print("\nSomething went wrong:", error)