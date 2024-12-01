import dearpygui.dearpygui as dpg


from config import FONT_INFO

class WrapManager:
    def __init__(self, app):
        self.app = app
        self.wrap_value = None

    def update_wrap_value(self, font_size):
        """Recalculates wrap value based on font size and updates chat history."""
        # Get the current window width
        window_width = dpg.get_viewport_client_width()
        
        # Calculate total horizontal padding from the main window
        total_padding = self.app.gui_manager.main_window.calculate_total_padding()
        
        # Calculate available width in pixels
        available_width = window_width - total_padding
        
        # Compute wrap value based on font size and available width
        wrap_value = FONT_INFO["font_ratio"] * available_width / font_size
        wrap_value = int(wrap_value)
        
        #print(f"Available width: {available_width}")
        #print(f"Wrap value: {wrap_value}")
        #print(f"Current font size: {font_size}")
        
        self.wrap_value = wrap_value
        
        # Update wrap value in chat history
        self.app.chat_history.update_wrap_value(wrap_value)