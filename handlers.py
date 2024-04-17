from aiogram.types import Message, FSInputFile, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder 
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from main import FSMNoteForm, FSMNoteDel
from generator_buttons import *
import aiosqlite as sq
from  aiogram import F
from aiogram import Bot
user_dict: dict[int, dict[str, str | int | bool]] = {}




async def start_handler(message: Message, bot:Bot):
    await message.answer("Привет! данный бот позволит тебе создать заметку.\nДобавить заметку по команде /addnote\nДоступно до 10 активных заметок.\nКоманда /help покажет возможности бота.")
    await bot.send_animation(message.chat.id,FSInputFile(path="C:\\Users\\Zver\\Desktop\\python\\notes_tg\\start.gif"))
async def help_command(message:Message):
    await message.answer('Список доступных команд:\n/addnote — добавить заметку\n/mynotes — выводит список ваших заметок\n/delnote — по выбору удаляет оставленную заметку\n/stopnotifications — останавливает отправку уведомлений\n/cancel — отменяет процесс создания заметки и её удаления')

async def MyNotes_handler(message: Message):
    await message.answer("Ваши заметки:")
    async with sq.connect('users.db') as db:
            cursor = await db.execute(f'SELECT user_id, txt, date from notes WHERE user_id = {message.from_user.id}')
            check = await cursor.fetchall()
            for i in check:
                await message.answer(f'Заметка: {i[1]}\nДата: {i[2]}')

#Процесс заполнения заметки
async def AddNote_handler(message: Message, state: FSMContext):
    await message.answer("Напишите текст к заметке, о которой вы бы не хотели забыть")
    await state.set_state(FSMNoteForm.note_text)
async def warning_addnote(message:Message):
    await message.answer('Вы уже создали 10 заметок, удалите одну, воспользовавшись командой /delnote, чтобы создать новую')


async def process_note_text(message:Message, state: FSMContext):
    await state.update_data(txt = message.text)
    keyboard = create_inline_kb(4, **dict_months)
    await message.answer(
        text = 'Отлично, теперь выберите месяц! Выбор прошеднего месяца запустит цикл отправки сообщения моментально',
        reply_markup = keyboard
    )
    await state.set_state(FSMNoteForm.note_month)
async def warning_not_text(message:Message):
    await message.answer('Мне нужны буквы!')

async def process_cur_month(callback: CallbackQuery, state: FSMContext):
    await state.update_data(date_month = callback.data)
    if int(callback.data) in [1,3,5,7,8,10,12]:
        keyboard = create_inline_kb(8, **dict_days_31)
    elif int(callback.data) == 2:
        keyboard = create_inline_kb(7, **dict_days_28)
    else:
        keyboard = create_inline_kb(6, **dict_days_30)
    await callback.message.edit_text(
        text = 'С месяцом определились, укажите день',
        reply_markup = keyboard
    )
    await state.set_state(FSMNoteForm.note_days)


async def process_cur_day(callback: CallbackQuery, state: FSMContext):
    await state.update_data(date_day = callback.data)
    keyboard = create_inline_kb(6, **dict_hours)
    await callback.message.edit_text(
        text = 'Осталось за малым\nВыберите час',
        reply_markup = keyboard
    )
    await state.set_state(FSMNoteForm.note_hours)


async def process_cur_hours(callback: CallbackQuery,state:FSMContext):
    await state.update_data(date_hours = callback.data)
    await callback.message.edit_text('Наконец, напишите минуты от 0-59.\n Перепишите по форме вновь, если допустили ошибку.\nЕсли желаете остановить заполение заметки - отправьте команду /cancel')
    await state.set_state(FSMNoteForm.note_minute)
async def warning_not_button(message:Message):
    await message.answer('Пожалуйста, пользуйтесь кнопками\n\nЕсли желаете остановить заполение заметки - отправьте команду /cancel')


async def process_cur_minute(message:Message,state:FSMContext):
    await state.update_data(date_minute = message.text)
    user_dict[message.from_user.id] = await state.get_data()
    async with sq.connect('users.db') as db:
        if len(message.text) == 1 and message.text in ['0','1','2','3','4','5','6','7','8','9']:
            await db.execute('INSERT INTO notes(user_id, txt, date) VALUES(?, ?, ?)', (message.from_user.id, user_dict[message.from_user.id]["txt"], "2024-"+user_dict[message.from_user.id]["date_month"]+'-'+user_dict[message.from_user.id]["date_day"]+' '+user_dict[message.from_user.id]["date_hours"]+':'+"0"+user_dict[message.from_user.id]["date_minute"],))
            await db.commit()
        else:
            await db.execute('INSERT INTO notes(user_id, txt, date) VALUES(?, ?, ?)', (message.from_user.id, user_dict[message.from_user.id]["txt"], "2024-"+user_dict[message.from_user.id]["date_month"]+'-'+user_dict[message.from_user.id]["date_day"]+' '+user_dict[message.from_user.id]["date_hours"]+':'+user_dict[message.from_user.id]["date_minute"],))
            await db.commit()
    await state.clear()
    user_dict.clear()
    await message.answer(f"Поздравляю, заметка успешно создана!")
async def warning_cur_minute(message:Message):
    message.answer('Пожалуйста, проследуйте инструкцией выше')


async def DelNote_handler(message: Message, state: FSMContext):
    await message.answer("напишите айди заметки, которую хотите удалить")
    async with sq.connect('users.db') as db:
        cursor = await db.execute(f'SELECT id, txt, date from notes WHERE user_id = {message.from_user.id}')
        check = await cursor.fetchall()
        for i in check:
            await message.answer(f'айди заметки: {i[0]}\nЗаметка: {i[1]}\nДата: {i[2]}')
    await state.set_state(FSMNoteDel.note_id)
async def process_note_del(message:Message, state: FSMContext):
    await state.update_data(note_id = message.text)
    user_dict[message.from_user.id] = await state.get_data()
    async with sq.connect('users.db') as db:
        cursor = await db.execute(f'SELECT user_id from notes WHERE id = {user_dict[message.from_user.id]["note_id"]}')
        check = await cursor.fetchone()
        if check[0] != message.from_user.id:
            await message.answer('Это айди не вашей заметки!\n Для повтовного удаления заметки напишите команду /delnote')
            await state.clear()
        else:
            await db.execute('DELETE FROM notes WHERE id = ?', (user_dict[message.from_user.id]["note_id"],))
            await db.commit()
            await state.clear()
            user_dict.clear()
            await message.answer(f"заметка успешно удалена!")
async def warning_NoOne(message:Message):
    await message.answer("у вас не обноруженно ни одной заметки, добавьте его командой /addnote")


async def StopNotifications_handler(message: Message):
    async with sq.connect('users.db') as db:
        await db.execute('DELETE FROM notifications WHERE user_id = ?', (message.from_user.id,))
        await db.commit()
    await message.answer("Уведомления успешно остановлены!")
async def warning_StopNotifications(message: Message):
    await message.answer("У вас нету активных уведомленний")


async def process_cancel_command(message: Message):
    await message.answer(
        text='Вы не создаёте и не удаляете заметку, отменять нечего.\nЧто бы оставить заметку напишите /addnote')
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Процедура создания заметку отменена!\n\n'
             'Чтобы снова перейти к созданию или удалению заметки — '
             'отправьте команду /addnote или /delnote'
    )
    await state.clear()