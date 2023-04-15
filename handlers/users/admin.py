import aiogram.utils.exceptions
import asyncpg
from datetime import datetime
from keyboards.default.admin_btns import admin_btns
from keyboards.default.main_menu import main_menu
from loader import db, dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup
from states.BigStates import Main
from data.config import ADMINS
from pytz import timezone
from .texts import stats


@dp.message_handler(text="/admin", chat_id=ADMINS, state="*")
async def showAdminBtn(message: Message, state: FSMContext):
    await message.answer("😊 Admin panelga xush kelibiz!", reply_markup=admin_btns())
    await state.set_state("get_action")


@dp.message_handler(text="➕ Manager qo'shish", state="get_action")
async def NewManager(message: Message, state: FSMContext):
    await message.answer("Menejer Telegram ID raqamini kiriting!", reply_markup=ReplyKeyboardRemove())
    await state.set_state("m_id")


@dp.message_handler(state="m_id")
async def sss(message: Message, state: FSMContext):
    ID = message.text
    if ID.isdigit():
        try:
            user = await bot.get_chat(ID)
            full_name = user.first_name + ' ' + user.last_name if user.last_name else user.first_name
            ID = int(ID)
            is_manager = await db.is_manager(ID)
            if is_manager:
                await message.answer(
                    "Bu menejer allaqachon bazada mavjud!\nBoshqa menejer qo'shishga harakat qib ko'rin!")
                return
            else:
                time_format = '%Y-%m-%d'
                formatted_now = datetime.now(timezone('Asia/Tashkent')).strftime(time_format)
                await db.add_manager(full_name, ID, formatted_now, 0)
                await message.answer("✅ Muvaffaqiyatli qo'shildi!", reply_markup=admin_btns())
                await state.set_state("get_action")
        except aiogram.utils.exceptions.ChatNotFound:
            await message.answer("Iltimos, qo'shmoqchi bo'lgan menejeringiz "
                                 "botga kirib, /start komandasini tersin!\n\nAks xolda bot meneger qo'sha olmaydi!")

    else:
        await message.answer("ID faqat raqamlardan tashkil topgan bo'ladi!\nQayta kiriting!")
        return


@dp.message_handler(text="Manager ON", state='get_action')
async def show_disabled(message: Message, state: FSMContext):
    managers_list = list()
    managers = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    off_managers = await db.show_off()
    if len(off_managers) == 0:
        await message.answer("Hamma menejerlar yoqilgan!", reply_markup=admin_btns())
        await state.set_state("get_action")
    else:
        for i in off_managers:
            managers_list.append(f"✅ {i[0]}")
        managers_list.append("⬅️ Orqaga")

        managers.add(*managers_list)

        await message.answer("Tanlang:", reply_markup=managers)
        await state.set_state("delete_on")


@dp.message_handler(state="delete_on")
async def switchON(message: Message, state: FSMContext):
    manager = message.text
    if manager == "⬅️ Orqaga":
        await message.answer("😊 Admin panelga xush kelibiz!", reply_markup=admin_btns())
        await state.set_state("get_action")
    else:
        manager = manager[2:]
        await db.switch_on_manager(manager)
        await message.answer("Yoqildi!", reply_markup=admin_btns())
        await state.set_state("get_action")


@dp.message_handler(text="Manager OFF", state='get_action')
async def show_disabled(message: Message, state: FSMContext):
    l = list()
    managers = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    off_managers = await db.show_on()
    if len(off_managers) == 0:
        await message.answer("Hamma menejerlar o'chgan!", reply_markup=admin_btns())
        await state.set_state("get_action")
    else:
        for i in off_managers:
            l.append(f"❌ {i[0]}")
        l.append("⬅️ Orqaga")

        managers.add(*l)

        await message.answer("Tanlang:", reply_markup=managers)
        await state.set_state("delete_off")


@dp.message_handler(state="delete_off")
async def switchON(message: Message, state: FSMContext):
    manager = message.text
    if manager == "⬅️ Orqaga":
        await message.answer("😊 Admin panelga xush kelibiz!", reply_markup=admin_btns())
        await state.set_state("get_action")

    else:
        manager = manager[2:]
        await db.switch_off_manager(manager)
        await message.answer("Ochirildi!", reply_markup=admin_btns())
        await state.set_state("get_action")


@dp.message_handler(text="❌ Manager o'chirish", state="get_action")
async def deleteManager(message: Message, state: FSMContext):
    deleted_mrkp = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m_list = list()
    managers = await db.show_both()
    if len(managers) == 0:
        await message.answer("O'chirishni amalga oshirib bo'lmaydi!\nMenejer yo'q!")
        await message.answer("😊 Admin panelga xush kelibiz!", reply_markup=admin_btns())
        await state.set_state("get_action")
    else:
        for i in managers:
            m_list.append(f"❌ {i[0]}")
        m_list.append("⬅️ Orqaga")

        deleted_mrkp.add(*m_list)

        await message.answer("O'chirmoqchi bo'lgan menegeringizni tanlang: ⬇️", reply_markup=deleted_mrkp)
        await state.set_state("deleteM")


@dp.message_handler(state="deleteM")
async def finishD(message: Message, state: FSMContext):
    manager_name = message.text
    if manager_name == "⬅️ Orqaga":
        await message.answer("😊 Admin panelga xush kelibiz!", reply_markup=admin_btns())
        await state.set_state("get_action")
    else:
        manager_name = manager_name[2:]
        await db.delete_manager(manager_name)
        await message.answer("✅ O'chirildi!", reply_markup=admin_btns())
        await state.set_state("get_action")


@dp.message_handler(text="🏡 Bosh menyu", state="get_action")
async def showAMenu(message: Message):
    await message.answer("🏡 Bosh menyu", reply_markup=main_menu())
    await Main.main_menu.set()


@dp.message_handler(text="📊 Statistika ko'rish", state="get_action")
async def showYear(message: Message, state: FSMContext):
    year_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    year_list = list()
    years_months = await db.getMonthYear()
    for i in years_months:
        year_list.append(str(i[1]))

    year_list.append("⬅️ Orqaga")
    year_markup.add(*year_list)

    await message.answer("Yil tanlang: ", reply_markup=year_markup)
    await state.set_state("get_year")


@dp.message_handler(state="get_year")
async def showMonth(message: Message, state: FSMContext):
    year = message.text
    if year == "⬅️ Orqaga":
        await message.answer("😊 Admin panelga xush kelibiz!", reply_markup=admin_btns())
        await state.set_state("get_action")

    else:
        await state.update_data(
            {"year": year}
        )
        months_list = list()
        month_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        months = await db.getMonthYear()
    
        for month in months:
            if str(months[0][0]) == str(1):
                months_list.append("Yanvar")
            elif str(months[0][0]) == str(2):
                months_list.append("Fevral")
            elif str(months[0][0]) == str(3):
                months_list.append("Mart")
            elif str(months[0][0]) == str(4):
                months_list.append("Aprel")
            elif str(months[0][0]) == str(5):
                months_list.append("May")
            elif str(months[0][0]) == str(6):
                months_list.append("Iyun")
            elif str(months[0][0]) == str(7):
                months_list.append("Iyul")
            elif str(months[0][0]) == str(8):
                months_list.append("Avgust")
            elif str(months[0][0]) == str(9):
                months_list.append("Sentyabr")
            elif str(months[0][0]) == str(10):
                months_list.append("Oktyabr")
            elif str(months[0][0]) == str(11):
                months_list.append("Noyabr")
            elif str(months[0][0]) == str(12):
                months_list.append("Dekabr")

        months_list.append("⬅️ Orqaga")
        month_markup.add(*months_list)
        await message.answer("Oyni tanlang:", reply_markup=month_markup)
        await state.set_state("get_month")


@dp.message_handler(state="get_month")
async def showStat(message: Message, state: FSMContext):
    month = message.text
    if month == "⬅️ Orqaga":
        await message.answer("😊 Admin panelga xush kelibiz!", reply_markup=admin_btns())
        await state.set_state("get_action")
    else:
        await state.update_data(
            {"month": month}
        )
        managers_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        managers_list = list()
        managers = await db.show_both()
        for manager in managers:
            user = await bot.get_chat(manager[1])
            full_name = user.first_name + ' ' + user.last_name if user.last_name else user.first_name
            managers_list.append(full_name)

        managers_list.append("⬅️ Orqaga")
        managers_markup.add(*managers_list)
        await message.answer("Menejerni tanlang:", reply_markup=managers_markup)
        await state.set_state("get_manager")





@dp.message_handler(state="get_manager")
async def finallyYES(message: Message, state: FSMContext):
    manager = message.text
    if manager == "⬅️ Orqaga":
        await message.answer("😊 Admin panelga xush kelibiz!", reply_markup=admin_btns())
        await state.set_state("get_action")
    else:
        data = await state.get_data()
        year = data.get('year')
        month = data.get('month')
        manager_id = await db.showByName(manager)
        if month == 'Aprel':
            sum = await db.showStatistcs(manager_id, year, 4)
            await message.answer(stats(manager, sum, year, month))
            managers_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            managers_list = list()
            managers = await db.show_both()
            for manager in managers:
                user = await bot.get_chat(manager[1])
                full_name = user.first_name + ' ' + user.last_name if user.last_name else user.first_name
                managers_list.append(full_name)

            managers_list.append("⬅️ Orqaga")
            managers_markup.add(*managers_list)
            await message.answer("Menejerni tanlang:", reply_markup=managers_markup)
            await state.set_state("get_manager")

        elif month == 'Yanvar':
            sum = await db.showStatistcs(manager_id, year, 1)
            await message.answer(stats(manager, sum, year, month))
            managers_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            managers_list = list()
            managers = await db.show_both()
            for manager in managers:
                user = await bot.get_chat(manager[1])
                full_name = user.first_name + ' ' + user.last_name if user.last_name else user.first_name
                managers_list.append(full_name)

            managers_list.append("⬅️ Orqaga")
            managers_markup.add(*managers_list)
            await message.answer("Menejerni tanlang:", reply_markup=managers_markup)
            await state.set_state("get_manager")

        elif month == 'Fevral':
            sum = await db.showStatistcs(manager_id, year, 2)
            await message.answer(stats(manager, sum, year, month))
            managers_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            managers_list = list()
            managers = await db.show_both()
            for manager in managers:
                user = await bot.get_chat(manager[1])
                full_name = user.first_name + ' ' + user.last_name if user.last_name else user.first_name
                managers_list.append(full_name)

            managers_list.append("⬅️ Orqaga")
            managers_markup.add(*managers_list)
            await message.answer("Menejerni tanlang:", reply_markup=managers_markup)
            await state.set_state("get_manager")

        elif month == 'Mart':
            sum = await db.showStatistcs(manager_id, year, 3)
            await message.answer(stats(manager, sum, year, month))
            managers_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            managers_list = list()
            managers = await db.show_both()
            for manager in managers:
                user = await bot.get_chat(manager[1])
                full_name = user.first_name + ' ' + user.last_name if user.last_name else user.first_name
                managers_list.append(full_name)

            managers_list.append("⬅️ Orqaga")
            managers_markup.add(*managers_list)
            await message.answer("Menejerni tanlang:", reply_markup=managers_markup)
            await state.set_state("get_manager")

        elif month == 'May':
            sum = await db.showStatistcs(manager_id, year, 5)
            await message.answer(stats(manager, sum, year, month))
            managers_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            managers_list = list()
            managers = await db.show_both()
            for manager in managers:
                user = await bot.get_chat(manager[1])
                full_name = user.first_name + ' ' + user.last_name if user.last_name else user.first_name
                managers_list.append(full_name)

            managers_list.append("⬅️ Orqaga")
            managers_markup.add(*managers_list)
            await message.answer("Menejerni tanlang:", reply_markup=managers_markup)
            await state.set_state("get_manager")

        elif month == 'Iyun':
            sum = await db.showStatistcs(manager_id, year, 6)
            await message.answer(stats(manager, sum, year, month))
            managers_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            managers_list = list()
            managers = await db.show_both()
            for manager in managers:
                user = await bot.get_chat(manager[1])
                full_name = user.first_name + ' ' + user.last_name if user.last_name else user.first_name
                managers_list.append(full_name)

            managers_list.append("⬅️ Orqaga")
            managers_markup.add(*managers_list)
            await message.answer("Menejerni tanlang:", reply_markup=managers_markup)
            await state.set_state("get_manager")

        elif month == 'Iyul':
            sum = await db.showStatistcs(manager_id, year, 7)
            await message.answer(stats(manager, sum, year, month))
            managers_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            managers_list = list()
            managers = await db.show_both()
            for manager in managers:
                user = await bot.get_chat(manager[1])
                full_name = user.first_name + ' ' + user.last_name if user.last_name else user.first_name
                managers_list.append(full_name)

            managers_list.append("⬅️ Orqaga")
            managers_markup.add(*managers_list)
            await message.answer("Menejerni tanlang:", reply_markup=managers_markup)
            await state.set_state("get_manager")

        elif month == 'Avgust':
            sum = await db.showStatistcs(manager_id, year, 8)
            await message.answer(stats(manager, sum, year, month))
            managers_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            managers_list = list()
            managers = await db.show_both()
            for manager in managers:
                user = await bot.get_chat(manager[1])
                full_name = user.first_name + ' ' + user.last_name if user.last_name else user.first_name
                managers_list.append(full_name)

            managers_list.append("⬅️ Orqaga")
            managers_markup.add(*managers_list)
            await message.answer("Menejerni tanlang:", reply_markup=managers_markup)
            await state.set_state("get_manager")

        elif month == 'Sentyabr':
            sum = await db.showStatistcs(manager_id, year, 9)
            await message.answer(stats(manager, sum, year, month))
            managers_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            managers_list = list()
            managers = await db.show_both()
            for manager in managers:
                user = await bot.get_chat(manager[1])
                full_name = user.first_name + ' ' + user.last_name if user.last_name else user.first_name
                managers_list.append(full_name)

            managers_list.append("⬅️ Orqaga")
            managers_markup.add(*managers_list)
            await message.answer("Menejerni tanlang:", reply_markup=managers_markup)
            await state.set_state("get_manager")

        elif month == 'Oktyabr':
            sum = await db.showStatistcs(manager_id, year, 10)
            await message.answer(stats(manager, sum, year, month))
            managers_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            managers_list = list()
            managers = await db.show_both()
            for manager in managers:
                user = await bot.get_chat(manager[1])
                full_name = user.first_name + ' ' + user.last_name if user.last_name else user.first_name
                managers_list.append(full_name)

            managers_list.append("⬅️ Orqaga")
            managers_markup.add(*managers_list)
            await message.answer("Menejerni tanlang:", reply_markup=managers_markup)
            await state.set_state("get_manager")

        elif month == 'Noyabr':
            sum = await db.showStatistcs(manager_id, year, 11)
            await message.answer(stats(manager, sum, year, month))
            managers_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            managers_list = list()
            managers = await db.show_both()
            for manager in managers:
                user = await bot.get_chat(manager[1])
                full_name = user.first_name + ' ' + user.last_name if user.last_name else user.first_name
                managers_list.append(full_name)

            managers_list.append("⬅️ Orqaga")
            managers_markup.add(*managers_list)
            await message.answer("Menejerni tanlang:", reply_markup=managers_markup)
            await state.set_state("get_manager")

        elif month == 'Dekabr':
            sum = await db.showStatistcs(manager_id, year, 12)
            await message.answer(stats(manager, sum, year, month))
            managers_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            managers_list = list()
            managers = await db.show_both()
            for manager in managers:
                user = await bot.get_chat(manager[1])
                full_name = user.first_name + ' ' + user.last_name if user.last_name else user.first_name
                managers_list.append(full_name)

            managers_list.append("⬅️ Orqaga")
            managers_markup.add(*managers_list)
            await message.answer("Menejerni tanlang:", reply_markup=managers_markup)
            await state.set_state("get_manager")
