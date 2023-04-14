from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    main = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📤 Buyurtma")
            ],
            [
                KeyboardButton(text="📌 Shartlar"),
                KeyboardButton(text="🏢 Filiallar")
            ],
            [
                KeyboardButton(text="☎️ Biz bilan aloqa"),
                KeyboardButton(text="🌐 Til o'zgartirish")
            ],
            [
                KeyboardButton(text="❓Tez-tez beriladigan savollar")
            ]
        ],
        resize_keyboard=True, one_time_keyboard=True
    )
    return main


def main_menu_rus():
    main = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📤 Заказать")
            ],
            [
                KeyboardButton(text="📌 Условия"),
                KeyboardButton(text="🏢 Филиалы")
            ],
            [
                KeyboardButton(text="☎️ Обратная связь"),
                KeyboardButton(text="🌐 Изменить язык")
            ],
            [
                KeyboardButton(text="❓Часто задаваемые вопросы")
            ]
        ],
        resize_keyboard=True, one_time_keyboard=True
    )
    return main


def contact():
    num = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="☎️ Raqam yuborish", request_contact=True)
            ]
        ], resize_keyboard=True, one_time_keyboard=True
    )
    return num


def contact_rus():
    num = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="☎️ Отправить номер", request_contact=True)
            ]
        ], resize_keyboard=True, one_time_keyboard=True
    )
    return num

