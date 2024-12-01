import dearpygui.dearpygui as dpg

from config import (
    DEFAULT_WIDTH,
    FONT_BUTTON_WIDTH,
    FONT_INFO,
    BUTTON_LABEL_INCREASE_FONT,
    BUTTON_LABEL_DECREASE_FONT,
    TEXT_LABEL_MAX_FONT,
    TEXT_LABEL_MIN_FONT,
)
from gui.wrap_manager import WrapManager



class FontManager:
    def __init__(self, app):
        self.app = app
        self.current_font_size = FONT_INFO["font_size"]
        self.font_size_message_id = None
        self.wrap_manager = WrapManager(app)  # Initialize WrapManager

    def create_fonts(self):
        # Create fonts using FONT_INFO and include Cyrillic characters
        with dpg.font_registry():
            for size in range(
                FONT_INFO["min_font_size"],
                FONT_INFO["max_font_size"] + 1,
                FONT_INFO["font_size_step"],
            ):
                with dpg.font(
                    FONT_INFO["default"],
                    size,
                    tag=f"font_{size}",
                ):
                    # Add Cyrillic font range hint
                    dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

    def create_font_size_adjustment_section(self, parent, tag):
        """Creates the font size adjustment section in the GUI."""
        with dpg.group(horizontal=True, parent=parent, tag=tag):
            # Remove the spacer here
            # dpg.add_spacer(width=DEFAULT_WIDTH - 100, tag="font_size_spacer")
            
            # Vertical group containing buttons and message
            with dpg.group():
                # Buttons in a horizontal group
                with dpg.group(horizontal=True):
                    dpg.add_button(
                        label=BUTTON_LABEL_INCREASE_FONT,
                        tag="increase_font_button",
                        width=FONT_BUTTON_WIDTH,
                        callback=self.increase_font_size,
                    )
                    dpg.add_button(
                        label=BUTTON_LABEL_DECREASE_FONT,
                        tag="decrease_font_button",
                        width=FONT_BUTTON_WIDTH,
                        callback=self.decrease_font_size,
                    )

                # Font size message below the buttons
                self.font_size_message_id = dpg.add_text("")
                # Apply the current font size to the message
                dpg.bind_item_font(
                    self.font_size_message_id, f"font_{self.current_font_size}"
                )

    def increase_font_size(self):
        """Increases the font size within limits."""
        if self.current_font_size < FONT_INFO["max_font_size"]:
            self.current_font_size += FONT_INFO["font_size_step"]
            if self.current_font_size > FONT_INFO["max_font_size"]:
                self.current_font_size = FONT_INFO["max_font_size"]
                dpg.set_value(self.font_size_message_id, "Max font")
            else:
                dpg.set_value(self.font_size_message_id, "")
            self.apply_font_size()
        else:
            print(f"Font size {self.current_font_size} is the maximum.")
            # Show "Max font" message
            dpg.set_value(self.font_size_message_id, TEXT_LABEL_MAX_FONT)

    def decrease_font_size(self):
        """Decreases the font size within limits."""
        if self.current_font_size > FONT_INFO["min_font_size"]:
            self.current_font_size -= FONT_INFO["font_size_step"]
            if self.current_font_size < FONT_INFO["min_font_size"]:
                self.current_font_size = FONT_INFO["min_font_size"]
                dpg.set_value(self.font_size_message_id, "Min font")
            else:
                dpg.set_value(self.font_size_message_id, "")
            self.apply_font_size()
        else:
            print(f"Font size {self.current_font_size} is the minimum.")
            # Show "Min font" message
            dpg.set_value(self.font_size_message_id, TEXT_LABEL_MIN_FONT)

    def apply_font_size(self):
        """Applies the current font size to relevant GUI components."""
        font_tag = f"font_{self.current_font_size}"
        if dpg.does_item_exist(font_tag):
            # Bind the font globally
            dpg.bind_font(font_tag)
            # Update the font size message
            if self.font_size_message_id and dpg.does_item_exist(self.font_size_message_id):
                dpg.bind_item_font(self.font_size_message_id, font_tag)
            # Apply font size to other GUI elements
            item_tags = [
                "input_text",
                "send_button",
                "image_path_input",
            ]
            for item_tag in item_tags:
                if dpg.does_item_exist(item_tag):
                    dpg.bind_item_font(item_tag, font_tag)
            # Apply font size to message widgets
            self.app.chat_history.apply_font_size()

            # Recalculate wrap value based on new font size using WrapManager
            self.wrap_manager.update_wrap_value(self.current_font_size)
        else:
            print(f"Font size {self.current_font_size} not found.")
