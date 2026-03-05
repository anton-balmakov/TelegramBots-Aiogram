# ТелеграмБот демонстрирует менюшки по командам и привязанные к ним ссылки, а также работу с описанными кнопками
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

import config
import DZ_TG04_keyboards as kb


bot = Bot(token=config.tltok)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message:Message):
    await message.answer("Выбери действие", reply_markup=kb.keyb1_inl)


@dp.message(F.text & ~F.text.startswith("/")) #отлавливает конкретное слово
async def answer (message:Message):
    if message.text == "Привет":
        await message.answer(f'Привет, {message.from_user.full_name}')
    elif message.text == "Пока":
        await message.answer(f'До свидания, {message.from_user.full_name}')

@dp.callback_query(F.data.in_({'hi', 'by'})) # для фильтрации добавили в скобки F.data.in_({'hi', 'by'}), чтобы не перехватывал все колбэки
async def answer_inl(callback: CallbackQuery):
    if callback.data == "hi":
        await callback.message.answer(f'Привет, {callback.from_user.full_name}')
    elif callback.data == "by":
        await callback.message.answer(f'До свидания, {callback.from_user.full_name}')

@dp.message(Command('links')) #отлавливает конкретное слово
async def answer_2(message:Message):
    await message.answer('Ну приветики, выбирай!!!', reply_markup=kb.keyb2_inl)

@dp.message(Command('dynamic')) #отлавливает конкретное слово
async def answer3_inl(message:Message):
    await message.answer('Динамические изменения В СтудиЮ!!!', reply_markup=kb.keyb3_inl)

@dp.callback_query(F.data == 'big')
async def answer3_inl2(callback: CallbackQuery):
    await callback.message.edit_text('Выбирай опцию', reply_markup=kb.keyb3_inl2)

@dp.callback_query(F.data.in_({'opc1', 'opc2'})) # для фильтрации добавили в скобки F.data......
async def answer_inl(callback: CallbackQuery):
    if callback.data == "opc1":
        await callback.message.answer('Опция 1')
    elif callback.data == "opc2":
        await callback.message.answer('Опция 2')


async def main():
    await dp.start_polling(bot) #Ваш бот использует polling — программа сама "стучится" к Telegram и распределяет сообщения по хендлерам по фильтрам.

if __name__ == '__main__':
    asyncio.run(main())
