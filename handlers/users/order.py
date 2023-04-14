import logging
import time
from datetime import datetime
from collections import deque
from pytz import timezone

from .texts import shartlar, active_card, afsus_card, \
    afsus_age, make_order, phone, product, send_success, lid, shartlar_rus, \
active_card_rus, afsus_age_rus, afsus_card_rus, make_order_rus, phone_rus, product_rus, send_success_rus
from loader import db, dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, ReplyKeyboardMarkup
from states.BigStates import Main
from keyboards.default.main_menu import main_menu, contact, main_menu_rus, contact_rus
from time import sleep
from keyboards.inline.start_btn import markup, yesno, yesno2, markup_rus, yesno_rus, yesno2_rus


firstl = ['📤 Buyurtma', '📤 Заказать']
@dp.message_handler(text=firstl, state=Main.main_menu)
async def fstep(message: Message, state: FSMContext):
    status = await db.getUser_status(message.from_user.id)
    lang = await db.getUser_lang(message.from_user.id)
    if lang == 'uz':
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

        # user_id = '5896332243'
        # await message.answer(f"<a href='tg://user?id={user_id}'>BEK</a>")


@dp.callback_query_handler(text='s', state="first_step")
async def finishFstep(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    lang = await db.getUser_lang(call.from_user.id)
    if lang == 'uz':
        await call.message.answer("Yoshingiz nechida? Yozing!", reply_markup=ReplyKeyboardRemove())
        await state.set_state("get_age")
    elif lang == 'ru':
        await call.message.answer("Сколько вам лет? Напишите!", reply_markup=ReplyKeyboardRemove())
        await state.set_state("get_age")




@dp.message_handler(state="get_age")
async def GetAge(message: Message, state: FSMContext):
    age = message.text
    lang = await db.getUser_lang(message.from_user.id)
    if lang == 'uz':
        if age.isdigit():
            age = int(age)
            if age >= 19:
                await db.update_user_age(message.from_user.id, age)
                await message.answer("Rasmiy ish joyingiz bormi?", reply_markup=yesno2())
                await state.set_state("get_work")
            else:
                await message.answer(afsus_age())
                await message.answer("🏡 Bosh menyu", reply_markup=main_menu())
                await Main.main_menu.set()

        else:
            await message.answer("Yoshingizni raqamlarda kiriting!\nMisol: 18, 23, 44")
            return
    elif lang == 'ru':
        if age.isdigit():
            age = int(age)
            if age >= 19:
                await db.update_user_age(message.from_user.id, age)
                await message.answer("Есть ли у вас официальное место работы?", reply_markup=yesno2_rus())
                await state.set_state("get_work")
            else:
                await message.answer(afsus_age_rus())
                await message.answer("🏡 Главное меню", reply_markup=main_menu_rus())
                await Main.main_menu.set()

        else:
            await message.answer("Введите свой возраст цифрами!\nПример: 18, 23, 44")
            return




@dp.callback_query_handler(text="bor", state="get_work")
async def getWorkYes(call: CallbackQuery, state: FSMContext):
    lang = await db.getUser_lang(call.from_user.id)
    await call.message.delete()
    await db.update_user_work(call.from_user.id, True)
    if lang == 'uz':
        await call.message.answer(active_card(), reply_markup=yesno())
        await state.set_state("get_card")
    elif lang == 'ru':
        await call.message.answer(active_card_rus(), reply_markup=yesno_rus())
        await state.set_state("get_card")


@dp.callback_query_handler(text="yoq", state="get_work")
async def getWorkNo(call: CallbackQuery, state: FSMContext):
    lang = await db.getUser_lang(call.from_user.id)
    await call.message.delete()
    await db.update_user_work(call.from_user.id, False)
    if lang == 'uz':
        await call.message.answer(active_card(), reply_markup=yesno())
        await state.set_state("get_card")
    elif lang == 'ru':
        await call.message.answer(active_card_rus(), reply_markup=yesno_rus())
        await state.set_state("get_card")



@dp.callback_query_handler(text="have", state="get_card")
async def getWorkYes(call: CallbackQuery, state: FSMContext):
    lang = await db.getUser_lang(call.from_user.id)
    await call.message.delete()
    await db.update_user_status(call.from_user.id, 0)
    await db.update_user_card(call.from_user.id, True)
    if lang == 'uz':
    # telefon so'rash
        await call.message.answer(product(), reply_markup=ReplyKeyboardRemove())
        await state.set_state("get_product")
    elif lang == 'ru':
        await call.message.answer(product_rus(), reply_markup=ReplyKeyboardRemove())
        await state.set_state("get_product")



@dp.callback_query_handler(text="havenot", state="get_card")
async def getWorkYes(call: CallbackQuery, state: FSMContext):
    lang = await db.getUser_lang(call.from_user.id)
    await call.message.delete()
    await db.update_user_status(call.from_user.id, 1)
    if lang == 'uz':
        await call.message.answer(afsus_card())
        await call.message.answer("🏡 Bosh menyu", reply_markup=main_menu())
        await Main.main_menu.set()
    elif lang == 'ru':
        await call.message.answer(afsus_card_rus())
        await call.message.answer("🏡 Главное меню", reply_markup=main_menu_rus())
        await Main.main_menu.set()




data_queue = deque()

a = list()


async def send_to_admins(num_admins):
    time_format = '%Y-%m-%d'
    formatted_now = datetime.now(timezone('Asia/Tashkent')).strftime(time_format)
    managers = await db.show_on()
    for i in managers:
        a.append(i[1])
    while data_queue:
        data = data_queue.popleft()

        admin = a[len(data) % num_admins]
        await bot.send_message(admin, data)
        await db.add_counter(admin, 1, formatted_now)


async def collect_data(data: str, num_admins):
    data_queue.append(data)
    if len(data_queue) == num_admins:
        await send_to_admins(num_admins)


@dp.message_handler(state="get_product")
async def getProduct(message: Message, state: FSMContext):
    name = await db.getUser_name(message.from_user.id)
    phoned = await db.getUser_phone(message.from_user.id)
    age = await db.getUser_age(message.from_user.id)
    work_status = await db.getUser_work(message.from_user.id)
    lang = await db.getUser_lang(message.from_user.id)
    mahsulot = message.text
    await state.update_data(
        {"product": mahsulot}
    )
    data = await state.get_data()
    product = data.get('product')
    if phoned == "null":
        if lang == 'uz':
            await message.answer(phone(), reply_markup=contact())
            await state.set_state("get_num")
        elif lang == 'ru':
            await message.answer(phone_rus(), reply_markup=contact_rus())
            await state.set_state("get_num")
    else:

        admins_list = list()
        time_format = '%Y-%m-%d'
        formatted_now = datetime.now(timezone('Asia/Tashkent')).strftime(time_format)
        await db.update_user_status(message.from_user.id, 1)
        managers = await db.show_on()
        for i in managers:
            admins_list.append(i[1])
        leng = len(admins_list)
        info = lid(name, phoned, age, work_status, product, message.from_user.id)
        await collect_data(info, leng)
        if lang == 'uz':
            await message.answer(send_success())
            await message.answer("🏡 Bosh menyu", reply_markup=main_menu())
            await Main.main_menu.set()
        elif lang == 'ru':
            await message.answer(send_success_rus())
            await message.answer("🏡 Главное меню", reply_markup=main_menu_rus())
            await Main.main_menu.set()



@dp.message_handler(content_types=['contact'], state="get_num")
async def getContact(message: Message, state: FSMContext):
    time_format = '%Y-%m-%d'
    formatted_now = datetime.now(timezone('Asia/Tashkent')).strftime(time_format)
    name = await db.getUser_name(message.from_user.id)
    age = await db.getUser_age(message.from_user.id)
    work_status = await db.getUser_work(message.from_user.id)
    data = await state.get_data()
    product = data.get('product')
    lang = await db.getUser_lang(message.from_user.id)

    managers_list = list()
    number = message.contact['phone_number']
    await db.update_user_phone(message.from_user.id, number)
    await db.update_user_status(message.from_user.id, 1)

    managers = await db.show_on()
    for i in managers:
        managers_list.append(i[1])
    leng = len(managers_list)
    info = lid(name, number, age, work_status, product, message.from_user.id)
    await collect_data(info, leng)
    if lang == 'uz':
        await message.answer(send_success())
        await message.answer("🏡 Bosh menyu", reply_markup=main_menu())
        await Main.main_menu.set()
    elif lang == 'ru':
        await message.answer(send_success_rus())
        await message.answer("🏡 Главное меню", reply_markup=main_menu_rus())
        await Main.main_menu.set()


@dp.message_handler(content_types=['text'], state="get_num")
async def getContact(message: Message, state: FSMContext):
    name = await db.getUser_name(message.from_user.id)
    age = await db.getUser_age(message.from_user.id)
    work_status = await db.getUser_work(message.from_user.id)
    data = await state.get_data()
    product = data.get('product')
    lang = await db.getUser_lang(message.from_user.id)
    managers_list = list()
    number = message.text
    length = len(number)
    if lang == 'uz':
        if length == 9:
            await db.update_user_phone(message.from_user.id, number)
            await db.update_user_status(message.from_user.id, 1)
            managers = await db.show_on()
            for i in managers:
                managers_list.append(i[1])
            leng = len(managers_list)
            info = lid(name, number, age, work_status, product, message.from_user.id)
            await collect_data(info, leng)

            await message.answer(send_success())
            await message.answer("🏡 Bosh menyu", reply_markup=main_menu())
            await Main.main_menu.set()
        else:
            await message.answer("Qayta kiriting!\n\nMisol: 901234567")
            return
    elif lang == 'ru':
        if length == 9:
            await db.update_user_phone(message.from_user.id, number)
            await db.update_user_status(message.from_user.id, 1)
            managers = await db.show_on()
            for i in managers:
                managers_list.append(i[1])
            leng = len(managers_list)
            info = lid(name, number, age, work_status, product, message.from_user.id)
            await collect_data(info, leng)

            await message.answer(send_success_rus())
            await message.answer("🏡 Главное меню", reply_markup=main_menu_rus())
            await Main.main_menu.set()
        else:
            await message.answer("Пожалуйста, введите еще раз!\n\nПример: 901234567")
            return