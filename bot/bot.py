import asyncio
import logging
import os
import sys

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
import pandas as pd

from parse import get_price
from db import save_user_data_to_db
from utils import validate_dataframe
from keyboards import upload_keyboard
from config import config

TOKEN = config.BOT_TOKEN.get_secret_value()
dp = Dispatcher(storage=MemoryStorage())


class UploadFile(StatesGroup):
    waiting_for_file = State()
    file_received = State()



@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f'⚙️ Для доступа к функционалу воспользуйтесь кнопками!',
                         reply_markup=upload_keyboard)


@dp.message(lambda message: message.text == '📂 Загрузить файл')
async def upload_button(message: Message, state: FSMContext):
    await message.answer('Прикрепите файл-таблицу, содержащую title, url, xpath')
    await state.set_state(UploadFile.waiting_for_file)


@dp.message(UploadFile.waiting_for_file)
async def process_file(message: Message, state: FSMContext, bot: Bot):
    """Получает файл от пользователя."""
    document = message.document
    await state.set_state(UploadFile.file_received)
    user_id = message.from_user.id
    file_path = f'uploads/{document.file_name}'

    try:
        df = await download_and_read_file(bot, document, file_path)
        valid_data, invalid_data = validate_dataframe(df)

        if invalid_data:
            await process_invalid_data(message, invalid_data)

        if valid_data:
            await process_valid_data(message, valid_data, user_id)

    except ValueError:
        await message.answer(
            '❌ Ошибка! Невозможно прочитать файл. Убедитесь, что файл является таблицей!')
    except Exception as e:
        await message.answer(f'❌ Ошибка: {str(e)}')
    finally:
        clean_up_file(file_path)


async def download_and_read_file(bot: Bot, document, file_path: str):
    """Скачивает файл и загружает его в DataFrame."""
    await bot.download(document, file_path)
    return pd.read_excel(file_path)


async def process_invalid_data(message: Message, invalid_data: list):
    """Формирует и отправляет ошибки валидации."""
    error_messages = '\n\n'.join(
        f'🚨 Ошибка валидации:\n\n'
        f'📌 <b>Title</b>: {row.get("title")}\n'
        f'🌐 <b>URL</b>: {row.get("url")}\n'
        f'📋 <b>XPath</b>: {row.get("xpath")}\n'
        f'❌ <b>Ошибка</b>: {row.get("validation_error")}'
        for row in invalid_data
    )
    await message.answer(
        f'⚠️ Обнаружены ошибки в следующих строках:\n\n{error_messages}')


async def process_valid_data(message: Message, valid_data: list, user_id: int):
    """Обрабатывает валидные данные: получает цену, вычисляет среднее, отправляет пользователю."""
    status_message = await message.answer('⏳ Начинаю обработку данных...')
    prices = []

    for data in valid_data:
        price = await get_price(data['url'], data['xpath'])
        data['price'] = price
        prices.append(price if isinstance(price, float) else None)

    user_data = '\n'.join(
        f'📌 <b>Title</b>: {data["title"]}\n'
        f'🌐 <b>URL</b>: {data["url"]}\n'
        f'📋 <b>XPath</b>: {data["xpath"]}\n'
        f'💰 <b>Цена</b>: {data["price"]}'
        for data in valid_data
    )

    average_price = sum(prices) / len(prices) if prices else 0

    await status_message.edit_text(f'✅ Ваши данные: \n\n{user_data}')
    await message.answer(f'📊 Средняя цена на товары: {average_price:.2f}')
    await save_user_data_to_db(valid_data, user_id)


def clean_up_file(file_path: str):
    """Удаляет загруженный файл."""
    if os.path.exists(file_path):
        os.remove(file_path)


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
