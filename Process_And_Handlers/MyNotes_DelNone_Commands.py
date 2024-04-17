from All_imports_For_Project.import_lib import *


#Общая функция для обоих комманд в случае, если в базе данной не найдено ни одной заметки пользователя
async def warning_NoOne(message:Message):
    await message.answer("у вас не обноруженно ни одной заметки, добавьте его командой /addnote")


#Реагирует на команду /mynotes. Выводит список заметок пользователя
async def MyNotes_handler(message: Message):
    await message.answer("Ваши заметки:")
    async with sq.connect('users.db') as db:
            cursor = await db.execute(f'SELECT user_id, txt, date from notes WHERE user_id = {message.from_user.id}')
            check = await cursor.fetchall()
            for i in check:
                await message.answer(f'Заметка: {i[1]}\nДата: {i[2]}')


#Реагирует на команду /delnote. Выводит список заметок. Удаляет заметку по id из базы данных(не удалит чужую заметку)
async def DelNote_handler(message: Message, state: FSMContext):
    await message.answer("напишите айди заметки, которую хотите удалить")
    async with sq.connect('users.db') as db:
        cursor = await db.execute(f'SELECT id, txt, date from notes WHERE user_id = {message.from_user.id}')
        check = await cursor.fetchall()
        for i in check:
            await message.answer(f'айди заметки: {i[0]}\nЗаметка: {i[1]}\nДата: {i[2]}')
    await state.set_state(FSMNoteDel.note_id)

#Команда /delnote заводит человека в состояние удаление заметки
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

