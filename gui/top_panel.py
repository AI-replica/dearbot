import dearpygui.dearpygui as dpg
from config import DEFAULT_WIDTH
from gui.font_manager import FontManager
from gui.cost_indicator import CostIndicator


class TopPanel:
    def __init__(self, app):
        self.app = app
        self.font_manager = app.font_manager
        self.tag = "top_panel"
        self.cost_indicator = CostIndicator(self.app, parent=self.tag)

    def create(self):
        with dpg.group(horizontal=True, tag=self.tag, parent="main_window"):
            # Create the font size adjustment section
            self.font_manager.create_font_size_adjustment_section(
                parent=self.tag, tag="font_size_adjustment_section"
            )
            # Create the cost indicator
            self.cost_indicator.create()

            # Add the "New chat" button after the cost indicator
            dpg.add_button(label="Creat new chat", callback=self.new_chat_callback)

    def update(self):
        # Update the cost indicator when needed
        self.cost_indicator.update()

    def new_chat_callback(self, sender, app_data, user_data):
        # Reset the conversation
        self.app.conversation_manager.reset_conversation()
        # Update the chat history display
        self.app.chat_history.update_chat_history()
