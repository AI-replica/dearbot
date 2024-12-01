import threading
from datetime import datetime

from config import THINKING_PLACEHOLDER
from utils.chat_logs import save_conversation_to_text_file
from utils.messages import prepare_user_message
from utils.messages import extract_message_text, process_assistant_response


class ConversationManager:
    def __init__(self, save_directory="conversations", save_filename=None):
        self.conversation = []
        self.conversation_lock = threading.Lock()
        self.save_directory = save_directory
        self.first_message7 = True

        # Generate a unique filename if not provided
        if save_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.save_filename = f"conversation_{timestamp}.txt"
        else:
            self.save_filename = save_filename

    def add_user_message(self, user_input):
        # Prepare the user's message
        include_context7 = self.first_message7
        user_message = prepare_user_message(
            user_input, include_additional_context7=include_context7
        )
        with self.conversation_lock:
            self.conversation.append(user_message)
            thinking_content = [{"type": "text", "text": THINKING_PLACEHOLDER}]
            self.conversation.append({"role": "assistant", "content": thinking_content})
            # Save the conversation after adding the user's message
            self.save_conversation(self.save_directory, self.save_filename)
            self.first_message7 = False

    def remove_thinking_placeholder(self):
        with self.conversation_lock:
            if (
                self.conversation
                and extract_message_text(self.conversation[-1]["content"])
                == THINKING_PLACEHOLDER
            ):
                self.conversation.pop()

    def process_assistant_response(self):
        # Process the assistant's response (this modifies self.conversation in place)
        process_assistant_response(self.conversation)
        # Save the conversation after the assistant's response
        self.save_conversation(self.save_directory, self.save_filename)

    """
    def add_image_message(self, image_path, input_text):
        try:
            image_message = prepare_image_message(image_path, input_text)
            with self.conversation_lock:
                self.conversation.append(image_message)
        except Exception as e:
            print(f"Error attaching image: {e}")
    """

    def save_conversation(self, directory, filename):
        """
        Save the current conversation to a text file.

        Args:
            directory (str): The path to the directory where the file will be saved.
            filename (str): The name of the file.
        """
        save_conversation_to_text_file(self.conversation, directory, filename)

    def reset_conversation(self):
        with self.conversation_lock:
            self.conversation.clear()
            # Generate a new unique filename for the new conversation
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.save_filename = f"conversation_{timestamp}.txt"
            self.first_message7 = True
