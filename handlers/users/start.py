import asyncpg
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.inline.start_btn import markup, yesno, yesno2, yesno_rus, markup_rus, yesno2_rus
from handlers.users.texts import shartlar, make_order, active_card,\
    shartlar_rus, active_card_rus, make_order_rus
from keyboards.inline.start_btn import markup
from states.BigStates import Main
from loader import dp, db
from keyboards.default.main_menu import main_menu, contact, main_menu_rus
from aiogram.dispatcher import FSMContext
from . texts import language
from keyboards.inline.language import language_btn


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: Message, state: FSMContext):
    is_user = await db.select_user(message.from_user.id)
    if is_user:
        lang = await db.getUser_lang(message.from_user.id)
        if lang == 'uz':
        # set language
            await message.answer("🏡 Bosh menyu", reply_markup=main_menu())
            await Main.main_menu.set()
        elif lang == 'ru':
            await message.answer("🏡 Главное меню", reply_markup=main_menu_rus())
            await Main.main_menu.set()

    else:
        if is_user is None:
            try:
                user = await db.add_user(telegram_id=message.from_user.id,
                                         full_name=message.from_user.full_name,
                                         username=message.from_user.username,
                                         )

            except asyncpg.exceptions.UniqueViolationError:
                pass

            await message.answer(language(), reply_markup=language_btn())
            await state.set_state("get_lang")

@dp.callback_query_handler(text_contains='u', state="get_lang")
async def setLang(call: CallbackQuery, state: FSMContext):
    lang = call.data
    await call.message.delete()
    await db.update_user_language(call.from_user.id, lang)
    if lang == 'uz':
        await call.message.answer("Iltimos, ismingizni kiriting: ⬇️", reply_markup=ReplyKeyboardRemove())
        await state.set_state("getname")
    elif lang == 'ru':
        await call.message.answer("Пожалуйста, введите свое имя: ⬇️", reply_markup=ReplyKeyboardRemove())
        await state.set_state("getname")


@dp.message_handler(state="getname")
async def updateName(message: Message, state: FSMContext):
    name = message.text
    await db.update_user_name(message.from_user.id, name)
    lang = await db.getUser_lang(message.from_user.id)
    if lang == 'uz':
        await message.answer("✅ Muvaffaqiyatli ro'yxatdan o'tdingiz!")
        status = await db.getUser_status(message.from_user.id)
        if status == 0:
        # New user
            name = await db.getUser_name(message.from_user.id)
            await message.answer(shartlar(name), reply_markup=ReplyKeyboardRemove())
            await message.answer(make_order(), reply_markup=markup())
            await state.set_state("first_step")
        else:
        # old user
            await message.answer(active_card(), reply_markup=yesno())
            await state.set_state("get_card")
    elif lang == 'ru':
        await message.answer("✅Вы успешно зарегистрировались!")
        status = await db.getUser_status(message.from_user.id)
        if status == 0:
            # New user
            name = await db.getUser_name(message.from_user.id)
            await message.answer(shartlar_rus(name), reply_markup=ReplyKeyboardRemove())
            await message.answer(make_order_rus(), reply_markup=markup_rus())
            await state.set_state("first_step")
        else:
            # old user
            await message.answer(active_card_rus(), reply_markup=yesno_rus())
            await state.set_state("get_card")


