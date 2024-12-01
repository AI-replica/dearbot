import dearpygui.dearpygui as dpg
import threading

from utils.markdown import CallInNextFrame
import queue

from config import (
    DEFAULT_HEIGHT,
    DEFAULT_WIDTH,
    PADDING,
    INPUT_HINT,
    DARK_THEME7,
)
from gui.call_when_started import CallWhenDPGStartedCustom

from gui.chat_history import ChatHistory
from gui.main_window import MainWindow
from gui.message_popup import MessagePopup
from utils.conversation_manager import ConversationManager
from gui.font_manager import FontManager
from gui.themes import create_themes

"""

TODO Some day maybe:
- show any kind of errors in the chat, e.g. in a separate text element
- a copy button for code blocks. Maybe extract the blocks and show them in a separate window or something, like Claude
- a button to switch between light and dark theme (currently done in the config.py file)
- slightly different background color for the user and the AI messages. Already works, but disabled for now, due to a very tricky bug (see multicolor_logic7)
- a button to regenerate the last response
- a button to collapse all messages into a very compact 1-message-per-line view for ease of navigation
"""


class EventHandler:
    def __init__(self, app):
        self.app = app
        self.conversation_manager = app.conversation_manager

        # Initialize the MessagePopup
        self.message_popup = MessagePopup(app)

        # Access to GUI manager
        self.gui_manager = app.gui_manager

    def send_message(self, sender, app_data):
        user_input = dpg.get_value("input_text").strip()
        if not user_input:
            return  # Do nothing if input is empty

        # Add the user's message to the conversation
        self.conversation_manager.add_user_message(user_input)

        # Update the chat history
        self.app.chat_history.update_chat_history()

        # Clear the input field
        dpg.set_value("input_text", "")

        # Hide the input field and send button
        dpg.hide_item("input_text")
        dpg.hide_item("send_button")

        # Show the thinking text
        dpg.show_item("thinking_text")

        # Start a new thread to get the assistant's response
        threading.Thread(target=self.get_assistant_response, daemon=True).start()

    def get_assistant_response(self):
        """Get the assistant's response in a separate thread."""
        # Process the assistant's response
        self.conversation_manager.process_assistant_response()

        # Enqueue GUI updates to be executed in the main thread
        self.app.update_queue.put(self.app.chat_history.update_chat_history)
        self.app.update_queue.put(
            self.app.gui_manager.main_window.top_panel.cost_indicator.update
        )

        # Enqueue re-enabling the controls
        self.app.update_queue.put(self.reenable_controls)

    def reenable_controls(self):
        """Re-enable the input field and send button."""
        # print("Re-enabling controls")  # For debugging purposes

        # Show the input field and send button
        dpg.show_item("input_text")
        dpg.show_item("send_button")

        # Hide the thinking text
        dpg.hide_item("thinking_text")

        # Clear the input field
        dpg.set_value("input_text", "")

        # Optionally reset the hint to INPUT_HINT
        dpg.configure_item("input_text", hint=INPUT_HINT)

        # Keep the focus on the input field in the next frame
        CallInNextFrame.append(lambda: dpg.focus_item("input_text"))


class GUIManager:
    def __init__(self, app):
        self.app = app

        # Initialize the MainWindow
        self.main_window = MainWindow(app)

        # Initialize the ImageInputPopup
        # self.image_input_popup = ImageInputPopup(app)

    def create_gui(self):
        self.main_window.create()
        # self.image_input_popup.create()

    def setup_viewport(self):
        dpg.create_viewport(
            title="Simple Chatbot", width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT
        )
        dpg.setup_dearpygui()
        dpg.show_viewport()

        # Set the resize callback for the viewport
        dpg.set_viewport_resize_callback(self.main_window.resize_callback)

        # Schedule the resize callback to adjust GUI elements after the first frame
        dpg.set_frame_callback(1, lambda: self.main_window.resize_callback(None, None))


class ChatApp:
    def __init__(self):
        # Initialize the conversation manager with save directory
        self.conversation_manager = ConversationManager(
            save_directory="conversations"
        )
        self.update_queue = queue.Queue()
        self.chat_history_wrap = DEFAULT_WIDTH - (PADDING * 2)  # Initialize wrap value

        # Initialize the chat history handler
        self.chat_history = ChatHistory(self)

        # Initialize the FontManager
        self.font_manager = FontManager(self)  # Pass self to FontManager

        # Initialize the GUI manager
        self.gui_manager = GUIManager(self)

        # Initialize the event handler
        self.event_handler = EventHandler(self)

        # Make the ImageInputPopup accessible via the app
        # self.image_input_popup = self.gui_manager.image_input_popup

        # Flag to check if initial resize has been done
        self.initial_resize_done = False

        # Theme-related attributes
        self.is_dark_theme = DARK_THEME7  # Default to dark theme
        self.current_theme = None

    def process_pending_gui_updates(self):
        while not self.update_queue.empty():
            func = self.update_queue.get()
            func()

    def check_items_ready(self):
        font_adjustment_height = dpg.get_item_rect_size("font_size_adjustment_section")[1]
        chat_controls_height = dpg.get_item_rect_size("chat_control_group")[1]
        if font_adjustment_height > 0 and chat_controls_height > 0:
            self.gui_manager.main_window.resize_callback(None, None)
            self.initial_resize_done = True

    def apply_theme(self):
        """Apply the current theme to all windows"""
        theme_tag = "dark_theme" if self.is_dark_theme else "light_theme"
        dpg.bind_theme(theme_tag)
        self.current_theme = theme_tag

    def run(self):
        dpg.create_context()
        self.font_manager.create_fonts()
        
        # Create themes before creating the GUI
        create_themes()
        
        self.gui_manager.create_gui()
        self.gui_manager.setup_viewport()
        self.font_manager.apply_font_size()
        
        # Apply the initial theme
        self.apply_theme()

        # Set focus to input_text after initial setup
        dpg.set_frame_callback(1, self.set_initial_focus)

        # Custom render loop
        while dpg.is_dearpygui_running():
            if not self.initial_resize_done:
                self.check_items_ready()
            self.process_pending_gui_updates()
            CallWhenDPGStartedCustom.execute()
            CallInNextFrame.execute()
            dpg.render_dearpygui_frame()

        dpg.destroy_context()

    def set_initial_focus(self):
        dpg.focus_item("input_text")


if __name__ == "__main__":
    app = ChatApp()
    app.run()
