from utils.files import find_txt_files, is_valid_path


SYSTEM_PROMPT = "You are a helpful assistant"

# If specified, the app will read the .txt files in the dir and always use them as context.
# Useful for stuff like providing the AI with documentation for your project etc.
CONTEXT_TEXTS_DIR_PATH = None


core_font = "assets/fonts/EBGaramond"  # a hyperlegible font that supports both Latin and Cyrillic
FONT_INFO = {
    "font_size": 32,
    "max_font_size": 40,  # don't make the min-max difference too big, as it massively slow downs the app loading
    "min_font_size": 20,
    "font_size_step": 4,  # Define the step size for font adjustments
    "font_ratio": 20,  # magic num to get the proper wrap value for a font size
    "default": f"{core_font}-Regular.ttf",
    "bold": f"{core_font}-Bold.ttf",
    "italic": f"{core_font}-Italic.ttf",
    "italic_bold": f"{core_font}-BoldItalic.ttf",
}

MARKDOWN_HIGHLIGHTING7 = True
COLLAPSE_USER_MESSAGES = True # Set true to avoid seeing massive context texts etc
DARK_THEME7 = True # Note: the light theme doesn't support code highlighting


# Default window dimensions
DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 600

# UI Element dimensions
INPUT_HEIGHT = 50
BUTTON_HEIGHT = INPUT_HEIGHT
BUTTON_WIDTH = 80
PADDING = 20
FONT_BUTTON_WIDTH = 30

IMG_THUMB_MAX_SIZE = 100

MESSAGE_POPUP_WIDTH = DEFAULT_WIDTH
MESSAGE_POPUP_HEIGHT = DEFAULT_HEIGHT


# Define button labels
BUTTON_LABEL_SEND = ">"
BUTTON_LABEL_INCREASE_FONT = "F+"
BUTTON_LABEL_DECREASE_FONT = "F-"
TEXT_LABEL_MAX_FONT = "Max!"
TEXT_LABEL_MIN_FONT = "Min!"
THINKING_PLACEHOLDER = "[Thinking...]"
INPUT_HINT = "Type your message here or paste an image path..."
TOTAL_COST_TEXT = "Spent this month: $"
SHORTENED_MESSAGE_PLACEHOLDER = "... [click for full message]"

# API costs
"""
https://www.anthropic.com/pricing#anthropic-api
https://docs.anthropic.com/en/docs/build-with-claude/vision

Claude 3.5 Sonnet:
"""
input_text_cost_mtok_usd = 3
output_text_cost_mtok_usd = 15
image_cost_denominator = 750  # e.g. tokens = (width px * height px)/750

######################### INCOMPATIBILITY FIXES #########################

if not DARK_THEME7:
    # becuase the markdown lib has hardcoded dark theme, switch it off
    # otherwise it will be white on white text
    MARKDOWN_HIGHLIGHTING7 = False
    print("Warning: markdown highlighting is disabled because the light theme doesn't support it")

######################### SANITY CHECKS #########################


def calculate_input_field_width(width):
    # Calculate the new width for the input field using constants
    input_field_width = width - BUTTON_WIDTH - (PADDING * 2)
    return input_field_width, BUTTON_WIDTH


# Sanity checks for font sizes
min_size = FONT_INFO["min_font_size"]
max_size = FONT_INFO["max_font_size"]
step = FONT_INFO["font_size_step"]
default_size = FONT_INFO["font_size"]

# Check that step size divides evenly into the font size range
if (max_size - min_size) % step != 0:
    raise ValueError(
        "font_size_step does not evenly divide the range between min_font_size and max_font_size."
    )

# Check that default font_size is compatible with min_font_size and font_size_step
if (default_size - min_size) % step != 0:
    raise ValueError(
        "font_size is not compatible with min_font_size and font_size_step. "
        "Ensure that (font_size - min_font_size) is divisible by font_size_step."
    )

# Calculate total number of font sizes
number_of_sizes = ((max_size - min_size) // step) + 1

# Warn if the total number of font sizes exceeds 10
if number_of_sizes > 10:
    print(
        "Warning: The total number of font sizes is greater than 10. "
        "This may cause performance issues."
    )


# Sanity checks for context texts dir
if CONTEXT_TEXTS_DIR_PATH is not None:
    if is_valid_path(CONTEXT_TEXTS_DIR_PATH):
        txt_files_list = find_txt_files(CONTEXT_TEXTS_DIR_PATH)
        if len(txt_files_list) == 0:
            raise ValueError(f"No .txt files found in the dir path {CONTEXT_TEXTS_DIR_PATH}")
    else:
        raise ValueError(f"Can't access the dir path {CONTEXT_TEXTS_DIR_PATH}")
