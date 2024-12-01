import dearpygui.dearpygui as dpg
import utils.markdown as dpg_markdown
from config import MARKDOWN_HIGHLIGHTING7

class ExtendedMarkdownText:
    def __init__(self, markdown_text: str):
        self.markdown_text = markdown_text
        self.group_id = None
        self.widget_id = None
        self.wrap = -1  # Initialize wrap value

    def add(self, wrap: int | float = -1, parent=0):
        self.wrap = wrap  # Store the wrap value

        # Validate parent
        if not dpg.does_item_exist(parent):
            print(f"Parent item {parent} does not exist.")
            parent = dpg.add_group()

        # Create a group to hold the markdown content
        self.group_id = dpg.add_group(parent=parent)

        # Render the markdown content immediately
        self.render_markdown(self.group_id, self.wrap)

        return self.group_id

    def update(self, markdown_text=None):
        # Delete previous markdown group
        if self.widget_id and dpg.does_item_exist(self.widget_id):
            dpg.delete_item(self.widget_id)
        else:
            print(f"Warning: widget_id {self.widget_id} does not exist or is invalid.")

        # Update the markdown text if provided
        if markdown_text is not None:
            self.markdown_text = markdown_text

        # Re-render the markdown content immediately
        self.render_markdown(self.group_id, self.wrap)

    def update_wrap(self, wrap_value):
        """Updates the wrap value and re-renders the markdown content."""
        self.wrap = wrap_value
        self.update()

    def render_markdown(self, parent_id, wrap=-1):
        # Ensure parent_id is valid
        if not dpg.does_item_exist(parent_id):
            print(f"Parent item {parent_id} does not exist.")
            return

        # Create a new group to hold the markdown content
        markdown_group = dpg.add_group(parent=parent_id)
        # Update widget_id to the new group
        self.widget_id = markdown_group

        if MARKDOWN_HIGHLIGHTING7:
            try:
                # Use DearPyGui_Markdown to render the markdown content
                dpg_markdown.add_text(
                    self.markdown_text,
                    parent=markdown_group,
                    wrap=wrap
                )
                # Apply the text theme to the markdown group
                dpg.bind_item_theme(markdown_group, "text_theme")

            except Exception as e:
                print(f"DearPyGui_Markdown encountered an exception: {e}")
                print("Falling back to standard DearPyGui text rendering.")
                # Use standard dearpygui to display the text
                dpg.add_text(
                    self.markdown_text,
                    parent=markdown_group,
                    wrap=wrap
                    # Do not set 'color', let it inherit from theme
                )
                # Apply the text theme
                dpg.bind_item_theme(markdown_group, "text_theme")
        else:
            # Use standard dearpygui to display the text
            dpg.add_text(
                self.markdown_text,
                parent=markdown_group,
                wrap=wrap
                # Do not set 'color', let it inherit from theme
            )
            # Apply the text theme
            dpg.bind_item_theme(markdown_group, "text_theme")