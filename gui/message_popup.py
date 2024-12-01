import dearpygui.dearpygui as dpg
from config import MESSAGE_POPUP_WIDTH, MESSAGE_POPUP_HEIGHT, PADDING


class MessagePopup:
    def __init__(self, app):
        self.app = app
        self.popup_id = "message_popup"
        self.input_text_id = "message_input_text"

    def show_message_popup(self, sender, app_data, user_data):
        """Display a popup with the content of the clicked message."""
        # Extract message content and role from user_data
        message_content = user_data["message_content"]
        role = user_data["role"]

        # Ensure message_content is a string
        if not isinstance(message_content, str):
            message_content = str(message_content)

        # Set the window label based on the role
        if role == "user":
            window_label = "Your Message"
        elif role == "assistant":
            window_label = "Assistant's Message"
        else:
            window_label = "Message"

        if not dpg.does_item_exist(self.popup_id):
            with dpg.window(
                label=window_label,
                modal=True,
                tag=self.popup_id,
                no_title_bar=False,
                width=MESSAGE_POPUP_WIDTH,
                height=MESSAGE_POPUP_HEIGHT,
            ):
                dpg.add_input_text(
                    label="",
                    default_value=message_content,
                    multiline=True,
                    readonly=False,
                    tag=self.input_text_id,
                    width=MESSAGE_POPUP_WIDTH - PADDING * 2,
                    height=MESSAGE_POPUP_HEIGHT - PADDING * 2,
                    no_horizontal_scroll=False,
                )
                dpg.add_button(
                    label="Close",
                    callback=lambda: dpg.hide_item(self.popup_id),
                    width=75,
                )
        else:
            # Update the window label and message content
            dpg.configure_item(self.popup_id, label=window_label)
            dpg.set_value(self.input_text_id, message_content)
            dpg.show_item(self.popup_id)
