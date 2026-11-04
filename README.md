## Ollama Cloud

The tutor chat and PDF question-answering responses can use Ollama Cloud. Set
`OLLAMA_CHAT_URL`, `LLM_MODEL`, and `OLLAMA_API_KEY` in your local `.env` file.
Use a cloud model name from Ollama's cloud model list, and keep the API key
private. The included `.env.example` shows the expected format.

PDFs are still processed and indexed locally: their text is extracted on your
machine and stored in the local ChromaDB database. When asking a PDF question,
the app sends retrieved text excerpts to the configured chat endpoint; it does
not upload the PDF or database to Ollama. PDF indexing still requires a local
Ollama instance with the `nomic-embed-text` model.
