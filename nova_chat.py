from tutor.tutor_engine import ask_tutor
from tutor.teaching_logic import create_learning_plan


def main():

    print("\n" + "=" * 55)
    print("             NOVA AI PERSONAL TUTOR")
    print("=" * 55)

    subject = input("\nEnter Subject: ").strip()
    topic = input("Enter Topic: ").strip()

    if not subject or not topic:
        print("Please enter both subject and topic.")
        return

    print("\n" + create_learning_plan(subject, topic))

    chat_history = []

    first_question = (
        f"Teach me {topic} in {subject} "
        "from absolute beginner level."
    )

    print("\nNOVA is preparing your lesson...\n")

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

    print("\n" + "=" * 55)
    print("           NOVA INTERACTIVE CHAT")
    print("=" * 55)
    print("Ask unlimited questions.")
    print("Type 'exit' ONLY when you want to stop.")
    print("=" * 55)

    while True:

        try:

            user_input = input("\nYou: ").strip()

            if user_input.lower() == "exit":
                print("\nNOVA: Thank you for learning with me!")
                print("Keep learning. Goodbye!")
                break

            if not user_input:
                print("Please enter a question.")
                continue

            print("\nNOVA is thinking...\n")

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

        except KeyboardInterrupt:
            print("\nNOVA: Session interrupted.")
            break

        except Exception as error:
            print("\nError:", error)


if __name__ == "__main__":
    main()