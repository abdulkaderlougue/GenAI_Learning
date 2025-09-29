"""
user asks --> frontend (telegram bot) --> backend (openai api) --> openai api (chat completions with tools) --> backend (call function) --> frontend (telegram bot)

BOTFATHER: https://t.me/BotFather
Create a new bot and get the token

"""
import logging
import asyncio, sys
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# # configure logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# # Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN) # will authenticate the bot
# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()
client = OpenAI(api_key=OPENAI_API_KEY)

class ChatSession:
    """Class to manage chat sessions and their message histories."""
    pass

class Reference:
    """Class to store previously response from the openai api."""
    def __init__(self) -> None :
        self.responses = []


# -----------------------------
references = Reference()
MODEL_3 = "gpt-3.5-turbo"
MODEL_4 = "gpt-4o-mini"

# command handler for /start
@dp.message(Command("start"))
async def welcome_message(message: types.Message):
    await message.answer(
        "Hello! I’m your AI assistant bot. Type /help to see commands."
    )

# Command handler for /help
@dp.message(Command("help"))
async def help_message(message: types.Message):
    help_commands = (
        "/start - Start the bot\n"
        "/help - Show this message\n"
        "/clear - Clear chat history"
    )
    await message.answer(f"Here are the commands:\n{help_commands}")

# Command handler for /clear
@dp.message(Command("clear"))
async def clear_history(message: types.Message):
    # Clear the chat history for this user
    references.responses = []
    await message.answer("Chat history cleared.")

# Handle any text message
@dp.message()
async def handle_message(message: types.Message):
    user_input = message.text
    chat_id = message.chat.id

    # Initialize chat history for this chat if not present
    if chat_id not in references.responses:
        references.responses.append({
            "chat_id": chat_id,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                }
            ]
        })

    # Find the chat history for this chat
    chat_history = next(item for item in references.responses if item["chat_id"] == chat_id)

    # Append user message to chat history
    chat_history["messages"].append({"role": "user", "content": user_input})

    # Get response from OpenAI
    response = client.chat.completions.create(
        model=MODEL_3,
        messages=chat_history["messages"],
        max_tokens=150,
        temperature=0.7,
    )

    assistant_message = response.choices[0].message

    # Append assistant message to chat history
    chat_history["messages"].append(assistant_message)

    # Send response back to user
    await message.answer(assistant_message.content)

async def main():
    # Start polling updates
    logging.info("Starting bot...")
    await dp.start_polling(bot, skip_updates=False)

if __name__ == "__main__":
    asyncio.run(main())