from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



def language_btn():
    btn = InlineKeyboardMarkup(row_width=2)
    btn.insert(InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data='uz'))
    btn.insert(InlineKeyboardButton(text="🇷🇺 Русский", callback_data='ru'))
    return btn