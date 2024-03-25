from aiogram.types import Message, FSInputFile
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from main import FSMNoteForm, FSMNoteDel
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


async def AddNote_handler(message: Message, state: FSMContext):
    await message.answer("Напишите текст к заметке, о которой вы бы не хотели забыть")
    await state.set_state(FSMNoteForm.note_text)
async def warning_addnote(message:Message):
    await message.answer('Вы уже создали 10 заметок, удалите одну, воспользовавшись командой /delnote, чтобы создать новую')

async def process_note_text(message:Message, state: FSMContext):
    await state.update_data(txt = message.text)
    await message.answer("Отлично, теперь запишите время в следующем виде:"
                        "\nDDMMhhmm(день, месяц, час, минут слитно. 12050653 = 12 мая 6 часов 53 минуты)")
    await state.set_state(FSMNoteForm.note_date)
async def warning_not_text(message:Message):
    await message.answer('Мне нужны буквы!')

async def process_note_date(message:Message, state:FSMContext):
    await state.update_data(date=message.text)
    user_dict[message.from_user.id] = await state.get_data()
    async with sq.connect('users.db') as db:
        await db.execute('INSERT INTO notes(user_id, txt, date) VALUES(?, ?, ?)', (message.from_user.id, user_dict[message.from_user.id]["txt"], "2024-"+user_dict[message.from_user.id]["date"][2:4]+'-'+user_dict[message.from_user.id]["date"][:2]+' '+user_dict[message.from_user.id]["date"][4:6]+':'+user_dict[message.from_user.id]["date"][6:],))
        await db.commit()
    await state.clear()
    await message.answer(f"Поздравляю, заметка успешно создана!")
async def warning_not_date(message:Message):
    await message.answer('Ещё раз, вам необходимо ввести дату по заданному формату выше')

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
        await db.execute('DELETE FROM notes WHERE id = ?', (user_dict[message.from_user.id]["note_id"],))
        await db.commit()
    await state.clear()
    await message.answer(f"заметка успешно удалена!")
async def warning_NoOne(message:Message):
    await message.answer("у вас необноруженно ни одной заметки, добавьте его командой /addnote")


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