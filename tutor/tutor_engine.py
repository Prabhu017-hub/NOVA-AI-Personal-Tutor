import requests

from ollama_config import (
    LLM_MODEL,
    OLLAMA_CHAT_URL,
    get_chat_headers,
)

SYSTEM_PROMPT = """
You are NOVA, an intelligent personal AI tutor.

Your responsibility is to teach students effectively.

Teaching Rules:

1. Always start with beginner-friendly explanations.
2. Explain concepts step by step.
3. Use simple English.
4. Give real-world examples.
5. Provide practical examples when teaching programming.
6. Never skip important concepts.
7. Ask questions to check student understanding.
8. If the student makes a mistake, explain it politely.
9. Adapt explanations to the student's knowledge level.
10. Never pretend the student understands without checking.

Your teaching structure:

1. Introduction
2. Definition
3. Simple Explanation
4. Real-world Example
5. Practical Example
6. Key Points
7. Understanding Check
8. Next Learning Step

Be friendly, patient and encouraging.
"""


def ask_tutor(question, chat_history=None):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    if chat_history:
        messages.extend(chat_history)

    messages.append({
        "role": "user",
        "content": question
    })

    try:

        response = requests.post(
            OLLAMA_CHAT_URL,
            json={
                "model": LLM_MODEL,
                "messages": messages,
                "stream": False
            },
            headers=get_chat_headers(),
            timeout=180
        )

        response.raise_for_status()

        result = response.json()

        return result["message"]["content"]

    except requests.exceptions.RequestException as error:

        return f"AI connection error: {error}"