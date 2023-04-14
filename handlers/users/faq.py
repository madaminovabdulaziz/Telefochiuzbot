from loader import db, dp
from aiogram.types import Message, ReplyKeyboardRemove
from states.BigStates import Main
from keyboards.default.main_menu import main_menu, main_menu_rus
from .texts import frequent, frequent_rus

faq_btns = ['❓Tez-tez beriladigan savollar', '❓Часто задаваемые вопросы']

@dp.message_handler(text=faq_btns, state=Main.main_menu)
async def showLocation(message: Message):
    lang = await db.getUser_lang(message.from_user.id)
    if lang == 'uz':
        await message.answer(frequent())
        await message.answer("🏡 Bosh menyu", reply_markup=main_menu())
        await Main.main_menu.set()
    elif lang == 'ru':
        await message.answer(frequent_rus())
        await message.answer("🏡 Главное меню", reply_markup=main_menu_rus())
        await Main.main_menu.set()