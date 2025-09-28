"""
this demostrates how to use tools with openai api.
docs: https://platform.openai.com/docs/guides/function-calling
"""

from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

def get_weather(longitude: float, latitude: float) -> str:
    """Get the weather for a given location."""
    res = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m",
        headers={"Content-Type": "application/json"},
        verify=False,
        
    )
    data = res.json()["current"] # extrat time, temperature, windspeed
    return data

def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """this function converts currency"""
    url = f"https://hexarate.paikama.co/api/rates/latest/{from_currency}?target={to_currency}"
    url2 = f"https://free.ratesdb.com/v1/rates?from={from_currency}&to={to_currency}"
    res = requests.get(
        url2,
        headers={"Content-Type": "application/json"},
        verify=False,
    )
    print(res.json())
    # rate = res.json()["data"]["mid"]
    rate = res.json()["data"]["rates"][to_currency]

    return {"conversion": rate * amount }

if __name__ == "__main__":
    MODEL_4 = "gpt-4o-mini"
    MODEL_3 = "gpt-3.5-turbo"
    # print(get_weather(77.5946, 12.9716))
    # print(convert_currency(100, "USD", "EUR"))

    openai_api_key = os.getenv("OPENAI_API_KEY")

    client = OpenAI(api_key=openai_api_key)

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

    system_message = "You are a helpful assistant with expertise in weather and currency conversion."
    user_message = "What's the weather like in Agboville? Also, How much is 1000 EUR in canada?"

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]

    response = client.chat.completions.create(
        model=MODEL_3,
        messages=messages,
        tools=tools
    )

    completion_message = response.model_dump()
    print(completion_message)
    print("Prompt tokens:", response.usage.prompt_tokens)
    print("Completion tokens:", response.usage.completion_tokens)
    print("Total tokens:", response.usage.total_tokens)

    # calling the tools
    def call_function(func_name, args):
        if func_name == "get_weather":
            return get_weather(**args)
        elif func_name == "convert_currency":
            return convert_currency(**args)
        
    
    messages.append(response.choices[0].message) # debug chat gpt


    for tool_call in response.choices[0].message.tool_calls:
        name = tool_call.function.name
        print(f"Calling function: {name}")
        args = json.loads(tool_call.function.arguments)
        print(f"With arguments: {args}")
        # messages.append(response.choices[0].message)

        result = call_function(name, args)
        messages.append(
            {"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(result)}
        ) 
        print(f"Function {name} called with arguments {args} returned {result}")
    print("Messages after tool calls:", messages)
    final_response = client.chat.completions.create(
        model=MODEL_3,
        messages=messages,
        # tools=tools
    )
    print(final_response.choices[0].message.content)

    print("Prompt tokens:", final_response.usage.prompt_tokens)
    print("Completion tokens:", final_response.usage.completion_tokens)
    print("Total tokens:", final_response.usage.total_tokens)