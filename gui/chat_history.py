import dearpygui.dearpygui as dpg

from gui.extended_markdown import ExtendedMarkdownText
from gui.message_gui import MessageGUI
from utils.markdown import CallInNextFrame


class ChatHistory:
    def __init__(self, app):
        self.app = app
        self.message_widgets = []  # Store instances of MessageGUI
        self.chat_history_id = None  # Will be initialized in create_chat_history()
        self.chat_history_markdown = None

    def create_chat_history(self, parent):
        # Create an ExtendedMarkdownText instance for chat history
        self.chat_history_markdown = ExtendedMarkdownText(markdown_text="")
        # Add the MarkdownText to the GUI with the initial wrap value
        self.chat_history_id = self.chat_history_markdown.add(
            parent=parent,
            wrap=self.app.chat_history_wrap,
        )

    def update_chat_history(self):
        wrap_value = self.app.chat_history_wrap

        # Safely get the conversation from ConversationManager
        with self.app.conversation_manager.conversation_lock:
            conversation = self.app.conversation_manager.conversation.copy()

        # Determine if we should scroll to bottom (if last message is from assistant)
        scroll_to_bottom_needed = False
        if conversation and conversation[-1]['role'] == 'assistant':
            scroll_to_bottom_needed = True

        # Clear previous chat history display
        self.clear_chat_history_display()

        # Ensure texture registry exists
        self.ensure_texture_registry()

        # Iterate over messages and display them
        for idx, message in enumerate(conversation):
            self.display_message(message, wrap_value)

        # Apply the current font size to all messages
        self.apply_font_size()

        # Scroll to the bottom if needed
        if scroll_to_bottom_needed:
            def scroll_to_bottom():
                max_scroll = dpg.get_y_scroll_max("chat_history_child_window")
                dpg.set_y_scroll("chat_history_child_window", max_scroll)

            # Use CallInNextFrame to ensure scrolling occurs after GUI updates
            CallInNextFrame.append(scroll_to_bottom)

    def clear_chat_history_display(self):
        if self.chat_history_id and dpg.does_item_exist(self.chat_history_id):
            dpg.delete_item(self.chat_history_id, children_only=True)
        self.message_widgets.clear()

    def ensure_texture_registry(self):
        if not dpg.does_item_exist("texture_registry"):
            with dpg.texture_registry(tag="texture_registry"):
                pass  # Empty registry

    def display_message(self, message, wrap_value):
        # Create a MessageGUI instance for this message
        message_gui = MessageGUI(
            message=message,
            parent=self.chat_history_id,
            wrap_value=wrap_value,
            app=self.app,
        )
        self.message_widgets.append(message_gui)

        # Add a separator after the message
        dpg.add_separator(parent=self.chat_history_id)

    def apply_font_size(self):
        """Applies the current font size to the message widgets."""
        for message_gui in self.message_widgets:
            message_gui.apply_font_size()

    def update_wrap_value(self, wrap_value):
        """Updates the wrap value and applies it to all message widgets."""
        for message_gui in self.message_widgets:
            message_gui.wrap_value = wrap_value
            message_gui.update()