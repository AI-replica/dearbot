import dearpygui.dearpygui as dpg

COLORS_LIGHT_THEME = {
    "window_background": (240, 240, 240, 255),
    "child_background": (240, 240, 240, 255),
    "text": (0, 0, 0, 255),
    "frame_background": (255, 255, 255, 255),
    "frame_background_hovered": (245, 245, 245, 255),
    "frame_background_active": (235, 235, 235, 255),
    "button": (220, 220, 220, 255),
    "button_hovered": (210, 210, 210, 255),
    "button_active": (200, 200, 200, 255),
    "border": (200, 200, 200, 255),
    "scrollbar_background": (240, 240, 240, 255),
    "scrollbar_grab": (210, 210, 210, 255),
    "scrollbar_grab_hovered": (200, 200, 200, 255),
    "scrollbar_grab_active": (190, 190, 190, 255),
}

COLORS_DARK_THEME = {
    "window_background": (25, 25, 25, 255),
    "child_background": (25, 25, 25, 255),
    "text": (255, 255, 255, 255),
    "frame_background": (40, 40, 40, 255),
    "frame_background_hovered": (45, 45, 45, 255),
    "frame_background_active": (50, 50, 50, 255),
    "button": (50, 50, 50, 255),
    "button_hovered": (60, 60, 60, 255),
    "button_active": (70, 70, 70, 255),
    "border": (110, 110, 110, 255),
    "scrollbar_background": (25, 25, 25, 255),
    "scrollbar_grab": (60, 60, 60, 255),
    "scrollbar_grab_hovered": (70, 70, 70, 255),
    "scrollbar_grab_active": (80, 80, 80, 255),
}

# Define background colors for user messages
USER_MESSAGE_BACKGROUND_COLOR_LIGHT = (
    245,
    245,
    245,
    255,
)  # Slightly lighter than default
USER_MESSAGE_BACKGROUND_COLOR_DARK = (
    35,
    35,
    35,
    255,
)  # Slightly lighter than default dark

# Mapping of descriptive names to Dear PyGui theme color constants
COLOR_NAMES_TO_DPG = {
    "window_background": dpg.mvThemeCol_WindowBg,
    "child_background": dpg.mvThemeCol_ChildBg,
    "text": dpg.mvThemeCol_Text,
    "frame_background": dpg.mvThemeCol_FrameBg,
    "frame_background_hovered": dpg.mvThemeCol_FrameBgHovered,
    "frame_background_active": dpg.mvThemeCol_FrameBgActive,
    "button": dpg.mvThemeCol_Button,
    "button_hovered": dpg.mvThemeCol_ButtonHovered,
    "button_active": dpg.mvThemeCol_ButtonActive,
    "border": dpg.mvThemeCol_Border,
    "scrollbar_background": dpg.mvThemeCol_ScrollbarBg,
    "scrollbar_grab": dpg.mvThemeCol_ScrollbarGrab,
    "scrollbar_grab_hovered": dpg.mvThemeCol_ScrollbarGrabHovered,
    "scrollbar_grab_active": dpg.mvThemeCol_ScrollbarGrabActive,
}


def create_theme(tag, color_scheme):
    with dpg.theme(tag=tag):
        with dpg.theme_component(dpg.mvAll):
            for name, color in color_scheme.items():
                if name in COLOR_NAMES_TO_DPG:
                    dpg.add_theme_color(COLOR_NAMES_TO_DPG[name], color)
                else:
                    print(f"Warning: '{name}' is not a valid color name.")


def create_themes():
    """Create and return both light and dark themes"""

    create_theme("light_theme", COLORS_LIGHT_THEME)
    create_theme("dark_theme", COLORS_DARK_THEME)

    background_type = "child_background"
    # User message themes
    create_theme(
        "user_message_theme_light",
        {background_type: USER_MESSAGE_BACKGROUND_COLOR_LIGHT},
    )

    create_theme(
        "user_message_theme_dark", {background_type: USER_MESSAGE_BACKGROUND_COLOR_DARK}
    )

    # Assistant message themes (optional)
    create_theme(
        "assistant_message_theme_light",
        {background_type: COLORS_LIGHT_THEME["child_background"]},
    )

    create_theme(
        "assistant_message_theme_dark",
        {background_type: COLORS_DARK_THEME["child_background"]},
    )


def create_text_theme():
    with dpg.theme(tag="text_theme"):
        with dpg.theme_component(dpg.mvAll):
            # Inherit 'dpg.mvThemeCol_Text' from the current theme
            pass
