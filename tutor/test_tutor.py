from tutor.tutor_engine import ask_tutor
from tutor.teaching_logic import create_learning_plan

print("=" * 50)
print("       NOVA AI PERSONAL TUTOR")
print("=" * 50)

subject = input("\nEnter Subject: ")
topic = input("Enter Topic: ")

print(create_learning_plan(subject, topic))

chat_history = []

print("\nNOVA is preparing your lesson...\n")

first_question = f"Teach me {topic} in {subject} from beginner level."

answer = ask_tutor(first_question, chat_history)

print("\nNOVA:", answer)

chat_history.append({
    "role": "user",
    "content": first_question
})

chat_history.append({
    "role": "assistant",
    "content": answer
})

print("\n" + "=" * 50)
print("       NOVA INTERACTIVE CHAT")
print("=" * 50)
print("Ask anything about your topic.")
print("Type exit to stop.")

while True:

    user_input = input("\nYou: ").strip()

    if user_input.lower() == "exit":
        print("\nNOVA: Happy learning! See you again.")
        break

    if not user_input:
        continue

    response = ask_tutor(user_input, chat_history)

    print("\nNOVA:", response)

    chat_history.append({
        "role": "user",
        "content": user_input
    })

    chat_history.append({
        "role": "assistant",
        "content": response
    })