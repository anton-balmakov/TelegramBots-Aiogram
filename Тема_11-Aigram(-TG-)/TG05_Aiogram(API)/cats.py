#Запускает Телеграмбот и при указании породы кошки на английском, парсит сайт cat и получает инфу о коте с фоткой
import asyncio
import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

bot = Bot(token=config.tltok)
dp = Dispatcher()

def get_cat_breeds():
    url = 'https://api.thecatapi.com/v1/breeds'
    headers = {'x-api-key' : config.cat_apikey}
    response = requests.get(url, headers=headers)
    return response.json()

def get_cat_img_bread(bread_id):
    url = f'https://api.thecatapi.com/v1/images/search?breed_ids={bread_id}'
    headers = {'x-api-key' : config.cat_apikey}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data[0]['url']

def get_bread_info(bread_name):
    breads = get_cat_breeds()
    for bread in breads:
        # print(f'{bread["name"]}')
        if bread['name'].lower() == bread_name.lower():
            return bread
    return None

@dp.message(CommandStart())
async def start(message:Message):
    await message.answer('Привет напиши мне название породы кошки и я пришлю ее фотку и информацию о ней')

@dp.message()
async def send_cat_info(message:Message):
    bread_name = message.text
    bread_info = get_bread_info(bread_name)
    if bread_info:
        cat_image = get_cat_img_bread(bread_info['id'])
        info = (f'Порода - {bread_info["name"]}\n'
                f'Описание - {bread_info["description"]}\n'
                f'Продолжительность жизни - {bread_info["life_span"]} лет')
        await message.answer_photo(photo=cat_image, caption=info)
    else:
        await message.answer('Порода не найдена')

async def main():
    await dp.start_polling(bot) #Ваш бот использует polling — программа сама "стучится" к Telegram и распределяет сообщения по хендлерам по фильтрам.

if __name__ == '__main__':
    asyncio.run(main())