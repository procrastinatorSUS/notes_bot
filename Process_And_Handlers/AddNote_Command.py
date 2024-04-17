from All_imports_For_Project.import_lib import *

#Отвечает на команду /addnote и вводит пользователя в сотояние заполнения заметки
async def AddNote_handler(message: Message, state: FSMContext):
    await message.answer("Напишите текст к заметке, о которой вы бы не хотели забыть")
    await state.set_state(FSMNoteForm.note_text)


#Если пользователь превысил лимит в 10 заметок
async def warning_addnote(message:Message):
    await message.answer('Вы уже создали 10 заметок, удалите одну, воспользовавшись командой /delnote, чтобы создать новую')
