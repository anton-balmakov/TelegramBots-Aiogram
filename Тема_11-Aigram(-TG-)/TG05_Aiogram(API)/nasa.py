#Запускает Телеграмбот и по команде парсит сайт nasa раздел ежедневные фото и получает фото дня
import asyncio
import requests
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from datetime import datetime, timedelta
import random

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

bot = Bot(token=config.tltok)
dp = Dispatcher()

def get_random_apod():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    randon_date = start_date + (end_date - start_date) * random.random()
    date_str = randon_date.strftime("%Y-%m-%d")

    url = f'https://api.nasa.gov/planetary/apod?api_key={config.nasa_apikey}&date={date_str}'
    response = requests.get(url)
    print(response.json())
    return response.json()

@dp.message(Command('fnasa'))
async def fnasa(message: Message):
    apod = get_random_apod()
    photo_url = apod['url']
    title = apod['title']
    await message.answer_photo(photo=photo_url, caption=title)


async def main():
    await dp.start_polling(bot) #Ваш бот использует polling — программа сама "стучится" к Telegram и распределяет сообщения по хендлерам по фильтрам.

if __name__ == '__main__':
    asyncio.run(main())