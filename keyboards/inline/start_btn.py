from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def markup():
    btn = InlineKeyboardMarkup(row_width=1)
    btn.insert(InlineKeyboardButton(text="✅ Boshlash", callback_data='s'))

    return btn


def yesno():
    btn = InlineKeyboardMarkup(row_width=2)
    btn.insert(InlineKeyboardButton(text="✅ Ha", callback_data="have"))
    btn.insert(InlineKeyboardButton(text="❌ Yo'q", callback_data="havenot"))

    return btn


def yesno2():
    btn = InlineKeyboardMarkup(row_width=2)
    btn.insert(InlineKeyboardButton(text="✅ Ha", callback_data="bor"))
    btn.insert(InlineKeyboardButton(text="❌ Yo'q", callback_data="yoq"))

    return btn




def markup_rus():
    btn = InlineKeyboardMarkup(row_width=1)
    btn.insert(InlineKeyboardButton(text="✅ Старт", callback_data='s'))

    return btn


def yesno_rus():
    btn = InlineKeyboardMarkup(row_width=2)
    btn.insert(InlineKeyboardButton(text="✅ Да", callback_data="have"))
    btn.insert(InlineKeyboardButton(text="❌ Нет", callback_data="havenot"))

    return btn


def yesno2_rus():
    btn = InlineKeyboardMarkup(row_width=2)
    btn.insert(InlineKeyboardButton(text="✅ Да", callback_data="bor"))
    btn.insert(InlineKeyboardButton(text="❌ Нет", callback_data="yoq"))

    return btn
