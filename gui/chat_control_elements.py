import dearpygui.dearpygui as dpg
from config import (
    BUTTON_HEIGHT,
    BUTTON_WIDTH,
    DEFAULT_WIDTH,
    INPUT_HEIGHT,
    INPUT_HINT,
    PADDING,
    BUTTON_LABEL_SEND,
    THINKING_PLACEHOLDER,
)

class ChatControlElements:
    def __init__(self, app, parent):
        self.app = app
        self.parent = parent  # Parent DPG item (e.g., "main_window")
        self.event_handler = app.event_handler  # Reference to the EventHandler
        # self.image_input_popup = app.image_input_popup  # Reference to the ImageInputPopup
        self.create_controls()

    def create_controls(self):
        # Wrap the controls in a group with a known tag
        with dpg.group(tag="chat_control_group", horizontal=True, parent=self.parent):
            # Input field and buttons side by side
            dpg.add_input_text(
                label="",
                tag="input_text",
                width=DEFAULT_WIDTH
                - BUTTON_WIDTH
                - (PADDING * 4),
                height=INPUT_HEIGHT,
                on_enter=True,
                callback=self.event_handler.send_message,
                hint=INPUT_HINT,
                multiline=True,
                ctrl_enter_for_new_line=True,
            )

            # dpg.add_button(
            #     label=BUTTON_LABEL_ATTACH_IMAGES,
            #     tag="attach_button",
            #     callback=self.image_input_popup.show,
            #     height=BUTTON_HEIGHT,
            #     width=ATTACH_BUTTON_WIDTH,
            # )

            dpg.add_button(
                label=BUTTON_LABEL_SEND,
                tag="send_button",
                callback=self.event_handler.send_message,
                height=BUTTON_HEIGHT,
                width=BUTTON_WIDTH,
            )

        # Add the thinking text, but keep it hidden initially
        dpg.add_text(
            THINKING_PLACEHOLDER,
            tag="thinking_text",
            parent=self.parent,
        )
        dpg.hide_item("thinking_text")
