from openai import OpenAI
from dotenv import load_dotenv
import os

from pydantic import BaseModel, ValidationError

load_dotenv()

# Define the response structure using Pydantic model
class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]


if __name__ == "__main__":
    openai_api_key = os.getenv("OPENAI_API_KEY")

    client = OpenAI(api_key=openai_api_key)

    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Extract the event information."},
            {"role": "user", "content": "Ali and Bob are going to a science fair today."}
        ],
        max_tokens=50,
        response_format=CalendarEvent,
    )

    try:
        calendar_event = response.choices[0].message.parsed
        print("Extracted Event:", calendar_event)
        print("Prompt tokens:", response.usage.prompt_tokens)
        print("Completion tokens:", response.usage.completion_tokens)
        print("Total tokens:", response.usage.total_tokens)
    except ValidationError as e:
        print("Validation Error:", e)
    


    