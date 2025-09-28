from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


if __name__ == "__main__":
    openai_api_key = os.getenv("OPENAI_API_KEY")

    openai = OpenAI(api_key=openai_api_key)
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello! How can you assist me today?"}
        ],
        max_tokens=50,
        temperature=0.7,
    )
    print(response.choices[0].message.content)