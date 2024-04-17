from All_imports_For_Project.import_lib import *

#Останавливает процесс отправки сообщений
async def StopNotifications_handler(message: Message):
    async with sq.connect('users.db') as db:
        await db.execute('DELETE FROM notifications WHERE user_id = ?', (message.from_user.id,))
        await db.commit()
    await message.answer("Уведомления успешно остановлены!")
async def warning_StopNotifications(message: Message):
    await message.answer("У вас нету активных уведомленний")


#Выходит из всех состояний(/delnote,/addnote)
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