#Запускает Телеграм бот и на оснвоании отввето создает список учеников в БД sqlite3
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import config
import sqlite3


bot = Bot(token=config.tltok)
dp = Dispatcher()

class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()

def init_db():
    conn = sqlite3.connect('school_date.db')
    cur  = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    clas TEXT NOT NULL)
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
    await message.answer("В какой класс ты ходишь?")
    await state.set_state(Form.grade)

@dp.message(Form.grade)
async def sch_clas(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)
    school_data = await state.get_data() #эта строка извлекает все что было сохраннено  в контексте (имя, возрас и клас) и делает словарь.

    conn = sqlite3.connect('school_date.db')
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO students (name, age, clas) VALUES (?, ?, ?)''', (school_data['name'], school_data['age'], school_data['grade']))
    conn.commit()
    conn.close()

async def main():
    await dp.start_polling(bot) #Ваш бот использует polling — программа сама "стучится" к Telegram и распределяет сообщения по хендлерам по фильтрам.

if __name__ == '__main__':
    asyncio.run(main())
