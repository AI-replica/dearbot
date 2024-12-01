import tiktoken
from config import (
    input_text_cost_mtok_usd,
    output_text_cost_mtok_usd,
    image_cost_denominator,
)
import os
from datetime import datetime


class CostManager:
    """
    A class to manage and track the costs of API calls.
    It logs each call's cost with a timestamp to a text file and can compute
    the total cost since the start of the current month.
    """

    LOG_FILE_PATH = 'api_costs.log'  # You can change this path as needed

    def __init__(self, log_file_path=None):
        if log_file_path:
            self.LOG_FILE_PATH = log_file_path
        # Ensure the log file exists
        if not os.path.exists(self.LOG_FILE_PATH):
            with open(self.LOG_FILE_PATH, 'w') as f:
                pass  # Create the file if it doesn't exist

    def log_call(self, cost):
        """
        Logs the cost of an API call to the log file with the current timestamp.

        Args:
            cost (float): The cost of the API call in USD.
        """
        timestamp = datetime.utcnow().isoformat()
        with open(self.LOG_FILE_PATH, 'a') as f:
            f.write(f"{timestamp},{cost}\n")

    def get_monthly_cost(self):
        """
        Calculates the total cost of API calls since the start of the current month.

        Returns:
            float: Total cost in USD since the start of the month.
        """
        total_cost = 0.0
        now = datetime.utcnow()
        month_start = datetime(now.year, now.month, 1)
        with open(self.LOG_FILE_PATH, 'r') as f:
            for line in f:
                try:
                    timestamp_str, cost_str = line.strip().split(',')
                    timestamp = datetime.fromisoformat(timestamp_str)
                    cost = float(cost_str)
                    if timestamp >= month_start:
                        total_cost += cost
                except ValueError:
                    # Skip lines that don't have the correct format
                    continue
        return total_cost


def calculate_api_call_cost(conversation, assistant_message):
    """
    Calculate the cost of the API request given the conversation and assistant's reply.

    The cost is calculated based on the number of tokens in the input and output text,
    and the dimensions of any images in the input.

    Returns a dictionary with the cost breakdown and total cost in USD.
    """

    # Initialize token counts
    input_text_tokens = 0
    input_image_tokens = 0
    output_text_tokens = 0

    # Create tokenizer (assuming 'cl100k_base' for Claude models)
    tokenizer = tiktoken.get_encoding("cl100k_base")

    # Helper function to count tokens in text
    def count_tokens(text):
        tokens = tokenizer.encode(text)
        return len(tokens)

    # Process input messages
    for message in conversation:
        content = message.get("content", [])
        for item in content:
            if item["type"] == "text":
                text = item["text"]
                input_text_tokens += count_tokens(text)
            elif item["type"] == "image":
                # Calculate image tokens
                width = item.get("width", 0)
                height = item.get("height", 0)
                if width > 0 and height > 0:
                    tokens = (width * height) / image_cost_denominator
                    input_image_tokens += tokens

    # Process assistant's reply
    output_text_tokens += count_tokens(assistant_message)

    # Calculate costs in USD
    input_text_cost = (input_text_tokens / 1e6) * input_text_cost_mtok_usd
    input_image_cost = (input_image_tokens / 1e6) * input_text_cost_mtok_usd
    output_text_cost = (output_text_tokens / 1e6) * output_text_cost_mtok_usd
    total_cost = input_text_cost + input_image_cost + output_text_cost

    # Return the cost breakdown
    return {
        "input_text_tokens": input_text_tokens,
        "input_image_tokens": input_image_tokens,
        "output_text_tokens": output_text_tokens,
        "input_text_cost_usd": input_text_cost,
        "input_image_cost_usd": input_image_cost,
        "output_text_cost_usd": output_text_cost,
        "total_cost_usd": total_cost,
    }