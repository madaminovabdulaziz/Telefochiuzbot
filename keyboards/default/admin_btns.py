from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def admin_btns():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="➕ Manager qo'shish")
            ],
            [
                KeyboardButton(text="❌ Manager o'chirish")
            ],
            [
                KeyboardButton(text="📊 Statistika ko'rish")
            ],
            [
                KeyboardButton(text="Manager ON"),
                KeyboardButton(text="Manager OFF")
            ],
            [
                KeyboardButton(text="🏡 Bosh menyu")
            ]
        ],
        resize_keyboard=True, one_time_keyboard=True
    )
    return markup