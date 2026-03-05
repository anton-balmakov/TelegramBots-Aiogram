#Телебот Спрашивает Имя, возраст и город, потом предоставляет погоду по данному городу и записывает все в БД

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import config
import sqlite3
import aiohttp
import logging


bot = Bot(token=config.tltok)
dp = Dispatcher()
ap_key = config.api_key

logging.basicConfig(level=logging.INFO)

class Form(StatesGroup):
    name = State()
    age = State()
    city = State()

def init_db():
    conn = sqlite3.connect('user_date.db')
    cur  = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS ustabl (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    city TEXT NOT NULL)
    ''')
    conn.commit()
    conn.close()

init_db()

@dp.message(CommandStart())
async def start(message:Message, state:FSMContext):
    await message.answer("Привет! Как тебя зовут?")
    await state.set_state(Form.name)

@dp.message(Form.name)
async def name(message:Message, state:FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Form.age)

@dp.message(Form.age)
async def age(message:Message, state:FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Изкакого ты города?")
    await state.set_state(Form.city)

@dp.message(Form.city)
async def city(message:Message, state:FSMContext):
    await state.update_data(city=message.text)
    user_data = await state.get_data() #эта строка извлекает все что было сохраннено  в контексте (имя, возрас и город) и делает словарь.

    conn = sqlite3.connect('user_date.db')
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO ustabl (name, age, city) VALUES (?, ?, ?)''', (user_data['name'], user_data['age'], user_data['city']))
    conn.commit()
    conn.close()

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.openweathermap.org/data/2.5/weather?q={user_data['city']}&appid={ap_key}&units=metric") as response:
            if response.status == 200:
                weather_data = await response.json()

                temp = weather_data['main']['temp']
                humidity = weather_data['main']['humidity']
                description = weather_data['weather'][0]['description']

                weather_report = (f"Город: {user_data['city']}\n"
                                  f"Температура: {temp}°C\n"
                                  f"Влажность: {humidity}%\n"
                                  f"Описание - {description}")
                await message.answer(weather_report)
            else:
                await message.answer("❌ Неудалось получить данные о погоде")
    await state.clear()

async def main():
    await dp.start_polling(bot) #Ваш бот использует polling — программа сама "стучится" к Telegram и распределяет сообщения по хендлерам по фильтрам.

if __name__ == '__main__':
    asyncio.run(main())
