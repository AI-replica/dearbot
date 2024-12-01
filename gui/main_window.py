import dearpygui.dearpygui as dpg

from gui.chat_control_elements import ChatControlElements
from gui.font_manager import FontManager
from gui.top_panel import TopPanel

from config import (
    DEFAULT_HEIGHT,
    DEFAULT_WIDTH,
    PADDING,
    calculate_input_field_width,
)


class MainWindow:
    def __init__(self, app):
        self.app = app

        # Access the FontManager instance from the app
        self.font_manager = app.font_manager

        # Initialize chat history
        self.chat_history = app.chat_history

        # Initialize the TopPanel
        self.top_panel = TopPanel(app)

        # Initialize chat control elements
        self.chat_control_elements = None  # Will be created in create()

    def create(self):
        # Create the main window
        with dpg.window(
            label="Chatbot",
            tag="main_window",
            pos=(0, 0),
            width=DEFAULT_WIDTH,
            height=DEFAULT_HEIGHT,
            no_title_bar=True,
            no_move=True,
        ):
            # Create the top panel
            self.top_panel.create()

            # Create a child window for the chat history
            with dpg.child_window(
                tag="chat_history_child_window",
                parent="main_window",
                autosize_x=True,
                horizontal_scrollbar=False,
                border=False,
            ):
                # Create chat history
                self.chat_history.create_chat_history(parent="chat_history_child_window")

            # Create chat control elements
            self.chat_control_elements = ChatControlElements(
                app=self.app,
                parent="main_window",
            )

    def resize_callback(self, sender, app_data):
        width = dpg.get_viewport_client_width()
        height = dpg.get_viewport_client_height()

        # Update the main window size
        dpg.set_item_width("main_window", width)
        dpg.set_item_height("main_window", height)

        # Update the sizes of input fields and buttons
        input_field_width, button_width = calculate_input_field_width(width)
        dpg.set_item_width("input_text", input_field_width)
        # dpg.set_item_width("attach_button", attach_button_width)
        dpg.set_item_width("send_button", button_width)

        # Update the width of the chat history child window
        dpg.set_item_width("chat_history_child_window", width - (PADDING * 2))

        # Get the heights of the top panel and chat controls
        top_panel_height = dpg.get_item_rect_size("top_panel")[1]
        chat_controls_height = dpg.get_item_rect_size("chat_control_group")[1]

        # If heights are zero (e.g., on first run), use default estimated heights
        if top_panel_height == 0:
            top_panel_height = 30  # Estimated height of the top panel
        if chat_controls_height == 0:
            chat_controls_height = 50  # Estimated height of chat control elements

        # Calculate the available height for the chat history
        chat_history_height = height - top_panel_height - chat_controls_height - (PADDING * 4)

        # Ensure the chat history height is not negative
        chat_history_height = max(chat_history_height, 100)

        # Set the height of the chat history child window
        dpg.set_item_height("chat_history_child_window", chat_history_height)

        # Calculate wrap width for chat history and update it
        chat_history_wrap = width - (PADDING * 4)
        self.app.chat_history_wrap = chat_history_wrap
        self.chat_history.update_wrap_value(chat_history_wrap)

    def calculate_total_padding(self):
        """Calculates total horizontal padding used in the main window."""
        # This should match the padding used in sizing elements in resize_callback
        return PADDING * 4  # Adjust if necessary
