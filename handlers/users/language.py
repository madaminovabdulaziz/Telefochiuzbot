from handlers.users.texts import language
from keyboards.default.main_menu import main_menu, main_menu_rus
from keyboards.inline.language import language_btn
from loader import db, dp, bot
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.dispatcher import FSMContext
from states.BigStates import Main

lang_txt = ["🌐 Изменить язык", "🌐 Til o'zgartirish"]


@dp.message_handler(text=lang_txt, state=Main.main_menu)
async def changeLang(message: Message, state: FSMContext):
    await message.answer(language(), reply_markup=language_btn())
    await state.set_state("gettil")


@dp.callback_query_handler(text_contains='u', state="gettil")
async def setLang(call: CallbackQuery, state: FSMContext):
    lang = call.data
    await call.message.delete()
    await db.update_user_language(call.from_user.id, lang)
    if lang == 'uz':
        await call.message.answer("🏡 Bosh menyu", reply_markup=main_menu())
        await Main.main_menu.set()
    elif lang == 'ru':
        await call.message.answer("🏡 Главное меню", reply_markup=main_menu_rus())
        await Main.main_menu.set()
