import dearpygui.dearpygui as dpg
from utils.cost_manager import CostManager
from config import TOTAL_COST_TEXT

class CostIndicator:
    def __init__(self, app, parent):
        self.app = app
        self.parent = parent
        self.tag = "cost_indicator"
        self.cost_manager = CostManager()
        self.total_cost = 0.0

    def get_total_cost_text(self):
        return f"{TOTAL_COST_TEXT}{self.total_cost:.5f}"

    def create(self):
        self.total_cost = self.cost_manager.get_monthly_cost()
        with dpg.group(horizontal=True, tag=self.tag, parent=self.parent):
            dpg.add_text(self.get_total_cost_text(), tag="cost_indicator_text")
            
            # Create a theme with grey text color
            with dpg.theme() as grey_text_theme:
                with dpg.theme_component(dpg.mvText):
                    dpg.add_theme_color(dpg.mvThemeCol_Text, (128, 128, 128, 255))
            # Bind the theme to the text item
            dpg.bind_item_theme("cost_indicator_text", grey_text_theme)

    def update(self):
        # Update the cost and refresh the displayed value
        self.total_cost = self.cost_manager.get_monthly_cost()
        dpg.set_value("cost_indicator_text", self.get_total_cost_text())
