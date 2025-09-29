import logging
import asyncio, sys
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

import os

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# # configure logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# # Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN) # will authenticate the bot

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()

# Command handler for /start
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("👋 Hello! I’m your simple bot. Type /help to see commands.")

# Command handler for /help
@dp.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer("Here are the commands:\n/start - Start the bot\n/help - Show this message")

# Handle any text message
@dp.message()
async def echo_handler(message: types.Message):
    await message.answer(f"You said: {message.text}")

async def main():
    # Start polling updates
    logging.info("Starting bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())