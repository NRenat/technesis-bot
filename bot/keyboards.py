from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

upload_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='📂 Загрузить файл')]],
    resize_keyboard=True
)
