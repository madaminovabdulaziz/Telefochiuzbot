from loader import db, dp
from aiogram.types import Message, ReplyKeyboardRemove
from states.BigStates import Main
from keyboards.default.main_menu import main_menu, main_menu_rus

filial_btn = ['🏢 Filiallar', '🏢 Филиалы']
@dp.message_handler(text=filial_btn, state=Main.main_menu)
async def showLocation(message: Message):
    lang = await db.getUser_lang(message.from_user.id)
    if lang == 'uz':
        await message.answer("<b>Filiallarimizni quyidagi link orqali bilib oling!</b> ⬇️")
        await message.answer("http://bit.ly/3STSXZK")
        await message.answer("🏡 Bosh menyu", reply_markup=main_menu())
        await Main.main_menu.set()

    elif lang == 'ru':
        await message.answer("<b>Узнайте наши филиалы по ссылке ниже!</b> ⬇️")
        await message.answer("http://bit.ly/3STSXZK")
        await message.answer("🏡 Главное меню", reply_markup=main_menu_rus())
        await Main.main_menu.set()