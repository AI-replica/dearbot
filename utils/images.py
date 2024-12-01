from pathlib import Path
from PIL import Image, ImageOps
import io
import base64
import numpy as np
import os
import sys
import subprocess

from config import IMG_THUMB_MAX_SIZE
from utils.files import is_valid_path

def is_image_path(path):
    # First, check if the stripped path ends with one of the image extensions
    image_extensions = (".png", ".jpg", ".jpeg", ".gif", ".webp")
    if not any(path.strip().lower().endswith(ext) for ext in image_extensions):
        return False
    return is_valid_path(path)


def resize_image(img, max_size_bytes):
    """Resize image to fit within max_size_bytes while maintaining aspect ratio"""
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    img_size = buffer.tell()

    if img_size <= max_size_bytes:
        return img

    # Calculate new dimensions to maintain aspect ratio
    ratio = (max_size_bytes / img_size) ** 0.5  # square root to get dimension ratio
    new_size = tuple(int(dim * ratio) for dim in img.size)
    return img.resize(new_size, Image.Resampling.LANCZOS)


def open_image(image_path):
    """Open the image from the given path."""
    return Image.open(image_path)


def correct_orientation(img):
    """
    Correct image orientation based on EXIF data.
    This is really important because otherwise the LLM will struggle to OCR the text, etc.
    """
    return ImageOps.exif_transpose(img)


def convert_to_rgb(img):
    """Convert image to RGB mode, handling images with alpha channels."""
    if img.mode == "RGBA":
        # Create a white background image
        background = Image.new("RGB", img.size, (255, 255, 255))
        # Paste the image onto the background using the alpha channel as mask
        background.paste(img, mask=img.split()[3])  # 3 is the alpha channel
        return background
    elif img.mode == "P":
        # For images in palette mode, convert directly to RGB
        return img.convert("RGB")
    else:
        return img.convert("RGB")


def resize_long_edge(img, max_long_edge):
    """
    Resize the image if its long edge exceeds max_long_edge.
    """
    width, height = img.size
    max_dimension = max(width, height)
    if max_dimension > max_long_edge:
        ratio = max_long_edge / max_dimension
        new_size = (int(width * ratio), int(height * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)
        print(f"Resized image to {new_size} due to max_long_edge constraint")
    return img


def resize_to_fit_size(img, max_size_bytes):
    """Resize image to fit within max_size_bytes while maintaining aspect ratio."""
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    img_size = buffer.tell()

    if img_size <= max_size_bytes:
        return img, img.size

    # Calculate new dimensions to maintain aspect ratio
    ratio = (max_size_bytes / img_size) ** 0.5  # square root to get dimension ratio
    new_size = tuple(int(dim * ratio) for dim in img.size)
    return img.resize(new_size, Image.Resampling.LANCZOS), new_size


def convert_to_base64(img):
    """Convert the image to a base64 encoded string."""
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)
    # Use standard_b64encode and omit any prefix
    return base64.standard_b64encode(buffer.read()).decode("utf-8")


def encode_image(image_path, max_long_edge=1568):
    """
    Note: according to Anthropic, the max long edge for images is 1568 pixels.
    https://docs.anthropic.com/en/docs/build-with-claude/vision

    All images are converted to JPEG as per Claude's requirements.
    """
    # Maximum file size (5MB in bytes)
    MAX_SIZE = 5 * 1024 * 1024

    # Open the image
    img = open_image(image_path)

    # Correct image orientation based on EXIF data
    img = correct_orientation(img)

    # Convert image to RGB (handles RGBA and P modes)
    img = convert_to_rgb(img)

    # Resize if the image's long edge exceeds max_long_edge
    img = resize_long_edge(img, max_long_edge)

    # Resize if necessary to reduce file size
    img, new_size = resize_to_fit_size(img, MAX_SIZE)

    # Convert to base64 (will be saved as JPEG)
    base64_str = convert_to_base64(img)

    return base64_str, new_size


def load_image_for_gui(image_path):
    """
    Load an image, correct its orientation based on EXIF data,
    and prepare it for display in DearPyGui.
    Returns width, height, and the flattened image data.
    """
    if not Path(image_path).exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    # Open the image using PIL
    img = Image.open(image_path)

    img = resize_long_edge(img, IMG_THUMB_MAX_SIZE)

    # Correct image orientation based on EXIF data
    img = ImageOps.exif_transpose(img)

    # Convert the image to RGBA
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    # Get image dimensions
    width, height = img.size

    # print(f"Thumb image dimensions: {width}x{height}")

    # Convert the image to a numpy array and flatten it
    img_data = np.array(img).astype(np.float32) / 255.0
    img_data = img_data.flatten()

    return width, height, img_data


def get_thumb_size(width, height, max_size):
    """
    Calculate the thumbnail size while maintaining aspect ratio.

    Args:
        width (int): Original image width.
        height (int): Original image height.
        max_size (int): Maximum size for width and height.

    Returns:
        tuple: (thumbnail_width, thumbnail_height)
    """
    aspect_ratio = width / height
    if width > height:
        thumbnail_width = max_size
        thumbnail_height = int(max_size / aspect_ratio)
    else:
        thumbnail_height = max_size
        thumbnail_width = int(max_size * aspect_ratio)
    return thumbnail_width, thumbnail_height


def open_image_external(image_path):
    try:
        if os.name == "nt":  # For Windows
            os.startfile(image_path)
        elif sys.platform == "darwin":  # For macOS
            subprocess.call(("open", image_path))
        else:  # For Linux and other operating systems
            subprocess.call(("xdg-open", image_path))
    except Exception as e:
        print(f"Error opening image {image_path}: {e}")
