from loader import db, dp
from aiogram.types import Message, ReplyKeyboardRemove
from states.BigStates import Main
from keyboards.default.main_menu import main_menu, main_menu_rus

aloqa_btns = ['☎️ Biz bilan aloqa', '☎️ Обратная связь']


@dp.message_handler(text=aloqa_btns, state=Main.main_menu)
async def showLocation(message: Message):
    lang = await db.getUser_lang(message.from_user.id)
    if lang == 'uz':
        await message.answer("<b>Onlayn sotib olish uchun +998787776777 raqamiga qo'ng'iroq qiling.\n"
                             "Bepul yetkazib beramiz!</b>")
        await message.answer("🏡 Bosh menyu", reply_markup=main_menu())
        await Main.main_menu.set()
    elif lang == 'ru':
        await message.answer("<b>Позвоните по телефону +998787776777, чтобы купить онлайн.\n"
                             "Доставляем бесплатно!</b>")
        await message.answer("🏡 Главное меню", reply_markup=main_menu_rus())
        await Main.main_menu.set()
