"""PLUGIN DESCRIPTION:

This plugin allows the user to send images to the chat.
The images are encoded in base64 and sent as image/jpeg.
"""

################################################################################
# GENERAL LOGIC FOR ALL PLUGINS:
################################################################################

def is_plugin_applicable(user_input):
    return plugin_specific_applicability_checker(user_input)


def augment_message_content(message_content):
    """
    The typical content looks like this:
    content = [{"type": "text", "text": user_input}]
    """
    user_input = message_content[0]["text"]
    if is_plugin_applicable(user_input):
        message_content = plugin_specific_content_augmenter(message_content)
    return message_content

################################################################################
# THE LOGIC THAT IS SPECIFIC TO THIS PLUGIN:
################################################################################

from utils.images import encode_image, is_image_path


def plugin_specific_applicability_checker(user_input):
    return is_image_path(user_input)


def plugin_specific_content_augmenter(message_content):
    """Handle image file processing and return content structure."""
    
    text_input = message_content[0]["text"]

    image_path = text_input
    
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

    message_content.extend(content)

    return message_content