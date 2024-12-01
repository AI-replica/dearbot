import os
import time

from utils.messages import extract_message_text

def save_conversation_to_text_file(conversation, directory, filename="conversation.txt"):
    """
    Save the conversation to a text file in the specified directory.

    Args:
        conversation (list): The conversation to save.
        directory (str): The path to the directory where the file will be saved.
        filename (str, optional): The name of the file. Defaults to "conversation.txt".
    """

    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    # Construct the full path to the file
    file_path = os.path.join(directory, filename)

    # Build the conversation text
    conversation_text = ""
    for message in conversation:
        role = message["role"].capitalize()
        content = message.get("content", [])
        timestamp = message.get("timestamp", int(time.time()))

        message_text = extract_message_text(content, shorten7=False)
        # Add the message to the conversation text
        conversation_text += f"{role} [{timestamp}]:\n{message_text}\n\n"
        # Add a highly visible divider
        conversation_text += "############################################################\n\n"

    already_exist = os.path.exists(file_path)
    if not already_exist:
        print(f"Saving the new conversation to {file_path}")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(conversation_text)



    