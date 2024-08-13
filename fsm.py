from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import logging, asyncio
from config import token

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

logging.basicConfig(level=logging.INFO)

class Form(StatesGroup):
    name = State()
    age = State()
    photo = State()
    
@dp.message(CommandStart())
async def start(message: Message, state : FSMContext):
    await state.set_state(Form.name)
    await message.reply("Привет, Как тебя зовут ?")
    
@dp.message(Form.name)
async def age(message:Message, state : FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(Form.age)
    await message.answer("Сколько тебе лет ?")
    
@dp.message(Form.age)
async def process_age(message:Message, state : FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста введите корректный возраста ")
        return
    
    age = int(message.text)
    if age < 18:
        await state.clear()
        await message.answer("Извините, этот бот доступен только лицам старше 18 лет, или повторите еще раз /start")
        return
    
    await state.update_data(age=age)
    await state.set_state(Form.photo)
    await message.answer("Отправьте мне свою фотографию")
    
@dp.message(Form.photo, F.content_type.in_(['photo']))
async def process_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data.get('name')
    age = data.get('age')
    photo = message.photo[-1].file_id
    
    await bot.send_message(
        message.chat.id,
        f'Твое имя: {name}\nТвой возраст: {age}',
    )
    
    await bot.send_photo(message.chat.id, photo)
    await state.clear()
    await message.answer("Спасибо! Все данные сохранены")
    
@dp.message(Command(commands=['cancle']))
@dp.message(F.text.lower() == 'отмена')
async def cmd_cancle(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Процесс отменен. Если хочешь заново начать нажми на /start")
    
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())