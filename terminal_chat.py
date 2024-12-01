from utils.ai_provider import get_claude_response
from utils.messages import (
    handle_assistant_response,
    prepare_user_message,
    print_instructions,
)


def chat():
    conversation = []

    print_instructions()

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "quit":
            break

        try:
            prepare_user_message(user_input)
            assistant_message = get_claude_response(conversation)
            handle_assistant_response(conversation, assistant_message)

        except Exception as e:
            print(f"Error processing message: {e}")
            continue


if __name__ == "__main__":
    chat()
