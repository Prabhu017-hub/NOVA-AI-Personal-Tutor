import os
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env")

OLLAMA_CHAT_URL = os.getenv(
    "OLLAMA_CHAT_URL",
    "http://localhost:11434/api/chat"
).strip()

LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2").strip()
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "").strip()


def get_chat_headers():
    if urlparse(OLLAMA_CHAT_URL).hostname == "ollama.com":
        if not OLLAMA_API_KEY:
            raise RuntimeError(
                "OLLAMA_API_KEY is required when using Ollama Cloud."
            )

        return {"Authorization": f"Bearer {OLLAMA_API_KEY}"}

    return {}
