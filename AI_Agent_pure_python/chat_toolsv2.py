"""
this demostrates how to use tools with openai api. version 2, an improvement over v1
a complete chat with tools example and better handling of tool calls and looping until final answer.
quit or exit to stop the chat.

docs: https://platform.openai.com/docs/guides/function-calling
"""

from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
import json
import time

load_dotenv()

def get_weather(longitude: float, latitude: float) -> str:
    """Get the weather for a given location."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    try:
        res = requests.get(
            url,
            headers={"Content-Type": "application/json"},
            timeout=10,
            verify=False,
        )
        data = res.json()["current"] # extrat time, temperature, windspeed
    except Exception as e:
        msg = {"error": str(e)}
        return msg
    return data

def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """this function converts currency"""
    # url = f"https://hexarate.paikama.co/api/rates/latest/{from_currency}?target={to_currency}"
    url = f"https://free.ratesdb.com/v1/rates?from={from_currency}&to={to_currency}"
    try:
        res = requests.get(
            url,
            headers={"Content-Type": "application/json"},
            timeout=10,
            verify=False,
        )
        # print(res.json())
        print( f"Conversion rate from {from_currency} to {to_currency}: {res.json()}" )
        # rate = res.json()["data"]["mid"]
        rate = res.json()["data"]["rates"][to_currency]
        
    except Exception as e:
        msg = {"error": str(e)}
        return msg

    return {"converted_amount": rate * amount }

# -----------------------------
# TOOL REGISTRY
# -----------------------------
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a given longitude and latitude",
            "parameters": {
                "type": "object",
                "properties": {
                    "longitude": {
                        "type": "number",
                        "description": "A number representing the longitude in decimal format",
                    },
                    "latitude": {
                        "type": "number",
                        "description": "A number representing the latitude in decimal format",
                    },
                    
                },
                "required": ["longitude", "latitude"],
                "additionalProperties": False,
            },
            "strict": True,
        }
            
    },
    {
        "type": "function",
        "function": {
            "name": "convert_currency",
            "description": "Convert a certain amount from one currency to another",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "number",
                        "description": "The amount of money to convert",
                    },
                    "from_currency": {
                        "type": "string",
                        "description": "The currency code of the currency to convert from (e.g., 'USD')",
                    },
                    "to_currency": {
                        "type": "string",
                        "description": "The currency code of the currency to convert to (e.g., 'EUR')",
                    },
                },
                "required": ["amount", "from_currency", "to_currency"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }
]

# -----------------------------
# FUNCTION CALL HANDLER
# -----------------------------
def call_function(func_name: str, args: dict):
    """ Call the appropriate function based on the function name and arguments provided."""
    if func_name == "get_weather":
        return get_weather(**args)
    elif func_name == "convert_currency":
        return convert_currency(**args)

# -----------------------------
# MAIN CHAT LOOP
# -----------------------------
def chat():
    # Load API key from environment variable or get from user
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        openai_api_key = input("Enter your OpenAI API key to start the chat: ").strip()
    
    client = OpenAI(api_key=openai_api_key)

    messages = [
        {
            "role": "system",
            "content": "You are an expert in weather and currency conversion. Use the tools when needed."
         },
    ]

    while True:
        DEBUG = True
        MODEL_3 = "gpt-3.5-turbo"
        MODEL_4 = "gpt-4o-mini"
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting chat.")
            break

        messages.append({"role": "user", "content": user_input})

        # Ask the model for a response with tools enabled
        response = client.chat.completions.create(
            model=MODEL_3,
            messages=messages,
            tools=tools,
        )

        assistant_message = response.choices[0].message

        messages.append(assistant_message)  # Add model's response to the chat history

        if DEBUG: print("Assistant first msg:", assistant_message.content)

        # Handle tool calls if any 
        if assistant_message.tool_calls: # check if there are tool calls
            for tool_call in assistant_message.tool_calls:
                try:

                    func_name = tool_call.function.name
                    func_args = json.loads(tool_call.function.arguments)

                    if DEBUG: print(f"Calling function: {func_name} with arguments: {func_args}")

                    # Call the appropriate function
                    result = call_function(func_name, func_args)

                    if DEBUG: print(f"Function {func_name} returned: {result}")

                    # Add the tool response to the messages
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result) # must be a string
                    })
                except Exception as e:
                    print(f"Error calling tool {func_name}: {e}")
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps({"error": str(e)})
                    })

            # After handling all tool calls, get a final response from the model
            final_response = client.chat.completions.create(
                model=MODEL_3,
                messages=messages,
                # tools=tools,  # Optionally include tools again to allow further calls, not needed in this case
            )

            final_message = final_response.choices[0].message
            messages.append(final_message)  # Add final response to chat history

            print("\nAssistant:", final_message.content)
        else:
            # Normal response without tool calls
            print("\nAssistant:", assistant_message.content)
        
if __name__ == "__main__":
    chat()
