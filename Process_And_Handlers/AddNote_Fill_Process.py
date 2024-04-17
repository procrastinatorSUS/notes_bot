from All_imports_For_Project.import_lib import *


#общая функция для всех процессов с кнопками в случае, где пользователь не использует кнопки
async def warning_not_button(message:Message):
    await message.answer('Пожалуйста, пользуйтесь кнопками\n\nЕсли желаете остановить заполение заметки - отправьте команду /cancel')


#Требуется написать сообщение в лимит 400 символов
async def process_note_text(message:Message, state: FSMContext):
    await state.update_data(txt = message.text)
    keyboard = create_inline_kb(4, **dict_months)
    await message.answer(
        text = 'Отлично, теперь выберите месяц! Выбор прошеднего месяца запустит цикл отправки сообщения моментально',
        reply_markup = keyboard
    )
    await state.set_state(FSMNoteForm.note_month)
#Отправляется в случае, если сообщение не текст(медиа-файл, стикер)
async def warning_not_text(message:Message):
    await message.answer('Мне нужны буквы!')


#В виде кнопок(инлайн клавиатуры) даётся выбор месяца(1-12)
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


#В виде кнопок(инлайн клавиатуры) даётся выбор день(количество дней зависит от месяца)
async def process_cur_day(callback: CallbackQuery, state: FSMContext):
    await state.update_data(date_day = callback.data)
    keyboard = create_inline_kb(6, **dict_hours)
    await callback.message.edit_text(
        text = 'Осталось за малым\nВыберите час',
        reply_markup = keyboard
    )
    await state.set_state(FSMNoteForm.note_hours)


#В виде кнопок(инлайн клавиатуры) даётся выбор часа суток
async def process_cur_hours(callback: CallbackQuery,state:FSMContext):
    await state.update_data(date_hours = callback.data)
    await callback.message.edit_text('Наконец, напишите минуты от 0-59.\n Перепишите по форме вновь, если допустили ошибку.\nЕсли желаете остановить заполение заметки - отправьте команду /cancel')
    await state.set_state(FSMNoteForm.note_minute)


#Требуется ввод однозначного/двузначного числа от 0-59 после чего все данные с базы данных сохраняются и отправляются в базу данных
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
#В случае, если минуты указаны не правильно(Не работает)
async def warning_cur_minute(message:Message):
    message.answer('Пожалуйста, проследуйте инструкцией выше')