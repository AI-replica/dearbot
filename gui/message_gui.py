import dearpygui.dearpygui as dpg
import os

from config import IMG_THUMB_MAX_SIZE, COLLAPSE_USER_MESSAGES
from gui.extended_markdown import ExtendedMarkdownText
from utils.messages import extract_message_text
from utils.images import load_image_for_gui, get_thumb_size, open_image_external

class MessageGUI:
    def __init__(self, message, parent, wrap_value, app):
        self.message = message
        self.parent = parent
        self.wrap_value = wrap_value
        self.app = app

        self.role = self.message["role"].capitalize()  # Capitalize role for label
        self.content = self.message["content"]

        shorten7 = False
        if self.role == "User" and COLLAPSE_USER_MESSAGES:
            shorten7 = True
        self.markdown_text = extract_message_text(self.content, shorten7=shorten7)
        self.popup_text = extract_message_text(self.content, shorten7=False)

        self.group_id = None     # Will store the group ID for this message
        self.md_text = None      # Will store the ExtendedMarkdownText object
        self.text_item_id = None  # Will store the item ID of the markdown text

        # Create the GUI elements for this message
        self.create_message_gui()

    def create_message_gui(self, multicolor_logic7=False):

        """
        The multicolor_logic logic is disabled for now, because I failed to fix
        the bug where the first message always has a very large height.
        Wasted many hours on this. Maybe I'll return to it later.
        """

        if multicolor_logic7:
            # Create a child window for the message to allow background color
            self.group_id = dpg.add_child_window(
                parent=self.parent,
                no_scrollbar=True,
                width=-1,
            )
            # Determine which theme to apply based on the role and current theme
            theme_suffix = "_dark" if self.app.is_dark_theme else "_light"

            if self.role.lower() == 'user':
                theme_tag = 'user_message_theme' + theme_suffix
            else:
                theme_tag = 'assistant_message_theme' + theme_suffix

            # Apply the theme to the message group
            dpg.bind_item_theme(self.group_id, theme_tag)

        else:
            self.group_id = dpg.add_group(parent=self.parent)


        # Add the role label
        self.add_role_label()

        # Add the message content with wrapping
        self.add_message_content()

        # Display images if any
        self.display_images()

        # Add click handler
        self.add_click_handler()

    def add_role_label(self):
        role_label = f"{self.role} says:"
        dpg.add_text(role_label, parent=self.group_id)

    def add_message_content(self):
        self.md_text = ExtendedMarkdownText(self.markdown_text)
        # Store the item ID of the markdown text
        self.text_item_id = self.md_text.add(parent=self.group_id, wrap=self.wrap_value)

    def display_images(self):
        for element in self.content:
            if element.get("type") == "image":
                image_path = element.get("path", "")
                self.display_image_thumbnail(image_path)

    def display_image_thumbnail(self, image_path):
        # Load and display the image thumbnail using the utility function
        try:
            width, height, img_data = load_image_for_gui(image_path)
            # Create a unique texture tag
            texture_tag = f"texture_{os.path.basename(image_path)}"
            # Check if the texture already exists
            if not dpg.does_item_exist(texture_tag):
                # Add the dynamic texture
                dpg.add_dynamic_texture(
                    width, height, img_data, tag=texture_tag, parent="texture_registry"
                )
            thumb_w, thumb_h = get_thumb_size(width, height, max_size=IMG_THUMB_MAX_SIZE)

            # Add the image to the message group
            image_id = dpg.add_image(texture_tag, parent=self.group_id, width=thumb_w, height=thumb_h)

            # Add click handler to the image thumbnail to open it externally
            user_data = {"image_path": image_path}

            def open_image_callback(sender, app_data, user_data):
                open_image_external(user_data["image_path"])

            handler = dpg.add_item_handler_registry()
            dpg.add_item_clicked_handler(
                button=dpg.mvMouseButton_Left,
                callback=open_image_callback,
                user_data=user_data,
                parent=handler,
            )
            dpg.bind_item_handler_registry(image_id, handler)

        except FileNotFoundError:
            print(f"Image file not found: {image_path}")
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")

    def add_click_handler(self):
        user_data = {"message_content": self.popup_text, "role": self.role.lower()}
        handler = dpg.add_item_handler_registry()

        def message_click_handler(sender, app_data, user_data):
            self.app.event_handler.message_popup.show_message_popup(sender, app_data, user_data)

        dpg.add_item_clicked_handler(
            button=dpg.mvMouseButton_Left,
            callback=message_click_handler,
            user_data=user_data,
            parent=handler,
        )
        # Bind the handler to the markdown text item instead of the group
        dpg.bind_item_handler_registry(self.text_item_id, handler)

    def apply_font_size(self):
        """Applies the current font size to the message content and re-renders if necessary."""
        font_tag = f"font_{self.app.font_manager.current_font_size}"
        if dpg.does_item_exist(font_tag):
            if dpg.does_item_exist(self.group_id):
                dpg.bind_item_font(self.group_id, font_tag)
            # Force re-rendering of the message to adjust wrapping
            self.update()
        else:
            print(f"Font size {self.app.font_manager.current_font_size} not found.")

    def update(self):
        """Updates the message display, particularly the wrap value."""
        if self.md_text:
            self.md_text.update_wrap(self.wrap_value)