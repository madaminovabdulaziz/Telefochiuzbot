from loader import dp, db, bot
from keyboards.default.main_menu import main_menu, main_menu_rus
from states.BigStates import Main
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from .texts import shartlar, shartlar_rus



shart_btn = ['📌 Shartlar', '📌 Условия']
@dp.message_handler(text=shart_btn, state=Main.main_menu)
async def showShart(message: Message, state: FSMContext):
    lang = await db.getUser_lang(message.from_user.id)
    name = await db.getUser_name(message.from_user.id)
    if lang == 'uz':
        await message.answer(shartlar(name))
        await message.answer("🏡 Bosh menyu", reply_markup=main_menu())
        await Main.main_menu.set()

    elif lang == 'ru':
        await message.answer(shartlar_rus(name))
        await message.answer("🏡 Главное меню", reply_markup=main_menu_rus())
        await Main.main_menu.set()
