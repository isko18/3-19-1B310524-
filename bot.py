import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

bot = Bot(token='7143865311:AAGLTrlaZ5Ko5AR8M3QOhSNf2vnqiZ-5-XM')
dp = Dispatcher()

@dp.message(Command('start'))
async def start(message:Message):
    await message.answer("Привет, как дела ?")
    
async def main():
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())