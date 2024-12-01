import anthropic

from config import SYSTEM_PROMPT
from utils.cost_manager import CostManager, calculate_api_call_cost


CLIENT = anthropic.Anthropic()
MODEL = "claude-3-5-sonnet-latest"

COST_MANAGER = CostManager() 


def get_claude_response(conversation, conversation_with_metadata, mock7=False):
    """Get response from Claude API"""

    if mock7:
        user_message = conversation[-1]["content"][0]["text"]
        res = f"User said: {user_message}"
    else:
        try:
            # print("Sending message to Claude")
            response = CLIENT.messages.create(
                model=MODEL,
                max_tokens=1000,
                temperature=0.8,
                system=SYSTEM_PROMPT,
                messages=conversation,
            )
            res = response.content[0].text

            # Calculate the API cost
            cost_info = calculate_api_call_cost(conversation_with_metadata, res)
            total_cost = cost_info["total_cost_usd"]
            #print(f"API Cost: ${total_cost:.6f}")
            #print(f" - Input Text Tokens: {cost_info['input_text_tokens']}")
            #print(f" - Input Image Tokens: {cost_info['input_image_tokens']}")
            #print(f" - Output Text Tokens: {cost_info['output_text_tokens']}")

            # Log the cost using CostManager
            COST_MANAGER.log_call(total_cost)

            # Optionally, display the total cost since the start of the month
            monthly_cost = COST_MANAGER.get_monthly_cost()
            #print(f"Total cost since the start of the month: ${monthly_cost:.6f}")

        except Exception as e:
            res = f"Error: {e}"
    return res
