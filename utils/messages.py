from pathlib import Path

from config import THINKING_PLACEHOLDER, SHORTENED_MESSAGE_PLACEHOLDER
from utils.ai_provider import get_claude_response

from utils.context import build_context_data  

from utils.plugins_manager import PluginManager

plugin_manager = PluginManager()


"""
def process_image_input(image_path):
    base64_image, _ = encode_image(image_path)
    # media_type = get_media_type(Path(image_path).suffix)

    content = [
        {
            "type": "image",
            "path": image_path,
            "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": base64_image,
            },
        }
    ]

    text_input = input("Add text description (optional): ").strip()
    if text_input:
        content.append({"type": "text", "text": text_input})

    print("Image added to message")
    return content
"""

def prepare_message_content(user_input):
    """Prepare message content from user input."""
    # Start with the standard textual content
    content = [{"type": "text", "text": user_input}]
    
    #if is_image_path(user_input):
    #    image_content = process_image_input_gui(user_input, "")
    #    content.extend(image_content)

    content = plugin_manager.process_input(content)
    
    return content


def handle_assistant_response(conversation, assistant_message):
    """Handle Claude's response and update conversation"""
    # print("\nClaude:", assistant_message)
    conversation.append(
        {"role": "assistant", "content": [{"type": "text", "text": assistant_message}]}
    )


def print_instructions():
    print("Chat with Claude (type 'quit' to exit)")
    print("You can also provide a path to an image file")
    print("-" * 40)


def extract_message_text(content, shorten7=False, shorten_len=30):
    if isinstance(content, list):
        texts = []
        for item in content:
            if item["type"] == "text":
                texts.append(item["text"])
            elif item["type"] == "image":
                # Placeholder for image; adjust as needed
                texts.append("![Image](image_placeholder.png)")
        res = "\n".join(texts)
    elif isinstance(content, dict) and content["type"] == "text":
        res = content["text"]
    else:
        res = str(content)  # Fallback in case of unexpected structure
    if shorten7:
        if res != THINKING_PLACEHOLDER:
            res = res.replace("\n", " ")
            if len(res) > shorten_len:
                res = res[:shorten_len] + SHORTENED_MESSAGE_PLACEHOLDER
    return res


"""
def process_image_input_gui(image_path, text_input):
    if not Path(image_path).is_file():
        print(f"The provided image path '{image_path}' does not exist. Treating input as text.")
        return [{"type": "text", "text": image_path}]
    
    base64_image, new_size = encode_image(image_path)

    width, height = new_size

    content = [
        {
            "type": "image",
            "path": image_path,
            "width": width,
            "height": height,
            "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": base64_image,
            },
        }
    ]

    if text_input:
        content.append({"type": "text", "text": text_input})

    return content
"""

def build_chat_history(conversation):
    # Build a Markdown string from the conversation
    chat_history = ""
    for message in conversation:
        role = message["role"]
        content = message["content"]

        # Extract the text from the content
        message_text = extract_message_text(content)

        if role == "user":
            chat_history += f"**You:** {message_text}\n\n"
        elif role == "assistant":
            chat_history += f"**Assistant:** {message_text}\n\n"
    return chat_history


def prepare_user_message(user_input, include_additional_context7=False):
    """Prepare the user's message content."""
    content = prepare_message_content(user_input)

    if include_additional_context7:
        context_data = build_context_data()
        if context_data:
            # Combine the user's input and context data into a single text element
            combined_text = content[0]["text"] + "\n" + context_data
            content = [{"type": "text", "text": combined_text}]

    return {"role": "user", "content": content}


"""
def prepare_image_message(image_path, input_text):
    content = process_image_input_gui(image_path, input_text)
    return {"role": "user", "content": content}
"""

def sanitize_conversation(conversation):
    # TODO: define allowed elements, remove everything else
    import copy

    sanitized_conversation = copy.deepcopy(conversation)
    for message in sanitized_conversation:
        content = message.get("content", [])
        for element in content:
            if element.get("type") == "image":
                if "path" in element:
                    del element["path"]
                if "width" in element:
                    del element["width"]
                if "height" in element:
                    del element["height"]
    return sanitized_conversation


def process_assistant_response(conversation_with_metadata):
    """Process the assistant's response based on the conversation."""
    # Remove the thinking indicator from the conversation in place
    conversation_with_metadata[:] = [
        msg
        for msg in conversation_with_metadata
        if extract_message_text(msg.get("content", [])) != THINKING_PLACEHOLDER
    ]

    # Sanitize the conversation before sending
    sanitized_conversation = sanitize_conversation(conversation_with_metadata)

    # Get assistant response using the sanitized conversation
    assistant_message = get_claude_response(sanitized_conversation, conversation_with_metadata)

    # Handle assistant response
    handle_assistant_response(conversation_with_metadata, assistant_message)

    return conversation_with_metadata

