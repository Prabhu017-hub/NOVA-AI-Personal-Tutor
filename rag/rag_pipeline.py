import requests

from ollama_config import (
    LLM_MODEL,
    OLLAMA_CHAT_URL,
    get_chat_headers,
)
from rag.vector_database import VectorDatabase


# ==========================================
# CONFIGURATION
# ==========================================


# ==========================================
# NOVA RAG PIPELINE
# ==========================================

class RAGPipeline:

    def __init__(self):

        self.vector_db = VectorDatabase()

        print("NOVA RAG Pipeline initialized!")

    # ======================================
    # RETRIEVE DOCUMENTS
    # ======================================

    def retrieve_context(self, question, top_k=5):

        results = self.vector_db.search(
            question,
            top_k=top_k
        )

        if not results:
            return "", []

        context_parts = []

        for index, result in enumerate(results, start=1):

            metadata = result["metadata"]

            source = metadata.get("source", "Unknown")

            page = metadata.get("page", "Unknown")

            text = result["text"]

            context_parts.append(
                f"""
                Source: {source}
                Page: {page}

                Content:
                {text}
                """
            )

        context = "\n\n".join(context_parts)

        return context, results

    # ======================================
    # GENERATE ANSWER
    # ======================================

    def generate_answer(self, question, context):

        system_prompt = """
        You are NOVA, an intelligent AI personal tutor.

        Your responsibilities:

        1. Explain concepts in simple language.
        2. Teach students step by step.
        3. Use examples wherever possible.
        4. Be accurate and educational.
        5. Use the supplied document context as
           the primary source of information.
        6. If the answer is not available in the
           document, clearly say so.
        7. Never invent document information.
        8. Distinguish general knowledge from
           information found in the document.
        """

        user_prompt = f"""
        STUDENT QUESTION:

        {question}

        DOCUMENT CONTEXT:

        {context}

        INSTRUCTIONS:

        Answer the student's question using
        the document context.

        Explain the answer clearly.

        Include the source page numbers when possible.

        If the document does not contain the answer,
        tell the student honestly.
        """

        response = requests.post(

            OLLAMA_CHAT_URL,

            json={

                "model": LLM_MODEL,

                "messages": [

                    {
                        "role": "system",
                        "content": system_prompt
                    },

                    {
                        "role": "user",
                        "content": user_prompt
                    }

                ],

                "stream": False,

                "options": {
                    "temperature": 0.3
                }

            },

            headers=get_chat_headers(),

            timeout=180

        )

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            details = response.text.strip()[:1000]
            if details:
                raise RuntimeError(
                    f"Ollama request failed: {details}"
                ) from error
            raise

        return response.json()["message"]["content"]

    # ======================================
    # COMPLETE RAG RESPONSE
    # ======================================

    def ask(self, question, top_k=5):

        if not question.strip():

            return {
                "answer": "Please enter a question.",
                "sources": []
            }

        # Step 1: Retrieve context

        context, results = self.retrieve_context(
            question,
            top_k
        )

        if not context:

            return {
                "answer": (
                    "I couldn't find relevant information "
                    "in your uploaded documents."
                ),
                "sources": []
            }

        # Step 2: Generate answer

        answer = self.generate_answer(
            question,
            context
        )

        # Step 3: Return answer and sources

        sources = []

        for result in results:

            sources.append({

                "source": result["metadata"].get(
                    "source", "Unknown"
                ),

                "page": result["metadata"].get(
                    "page", "Unknown"
                ),

                "distance": result["distance"]

            })

        return {

            "answer": answer,

            "sources": sources

        }


# ==========================================
# TEST PIPELINE
# ==========================================

if __name__ == "__main__":

    nova = RAGPipeline()

    print("\n" + "=" * 50)

    print("         NOVA AI DOCUMENT TUTOR")

    print("=" * 50)

    while True:

        question = input("\nYou: ").strip()

        if question.lower() in ["exit", "quit"]:

            print("\nNOVA: Goodbye! Keep learning!")

            break

        if not question:
            continue

        print("\nNOVA is thinking...\n")

        try:

            result = nova.ask(question)

            print("\nNOVA:", result["answer"])

            print("\nSOURCE REFERENCES:")

            for source in result["sources"]:

                print(
                    f"PDF: {source['source']} | "
                    f"Page: {source['page']}"
                )

        except Exception as error:

            print("\nError:", error)