from All_imports_For_Project.MultiProc_Async_log import * #импорты библиотек async, logging, multiprocess
from All_imports_For_Project.Aiogram_libs_Main import * #импорты для aiogram
from All_imports_For_Project.self_imports_Main import * #импорты файлов из проекта
from All_imports_For_Project.FSM_states_Main import * #все состояния в которые входит пользователь 

async def main():
    bot = Bot(token='6552323918:AAHexHWmhL-khv6iL1J_6Mc2BQB-pXqeS5o', parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    await set_commands(bot)
    
    #основные команды: старт, отключение режима заполнения заметки и добавшение заметки с проверкой на то, что в базе данных их не больше 10
    dp.message.register(start_handler, Command(commands='start'), StateFilter(default_state))
    dp.message.register(help_command, Command(commands='help'), StateFilter(default_state))
    dp.message.register(process_cancel_command, Command(commands='cancel'),StateFilter(default_state))
    dp.message.register(process_cancel_command_state, Command(commands='cancel'),~StateFilter(default_state))
    dp.message.register(AddNote_handler, Command(commands='addnote'),StateFilter(default_state), CheckDatabaseLess())
    dp.message.register(warning_addnote, Command(commands='addnote'),StateFilter(default_state))
    

    #ввод текста заметки и проверка, что это текст
    dp.message.register(process_note_text, StateFilter(FSMNoteForm.note_text),F.text and F.text.len() < 400)
    dp.message.register(warning_not_text, StateFilter(FSMNoteForm.note_text))
    #ввод месяца
    dp.callback_query.register(process_cur_month, StateFilter(FSMNoteForm.note_month),F.data.in_([i for i in dict_months.keys()]))
    dp.message.register(warning_not_button, StateFilter(FSMNoteForm.note_month))
    #ввод дня
    dp.callback_query.register(process_cur_day, StateFilter(FSMNoteForm.note_days),F.data.in_([i for i in dict_days_31.keys()]))
    dp.message.register(warning_not_button, StateFilter(FSMNoteForm.note_days))
    #ввод часа
    dp.callback_query.register(process_cur_hours,StateFilter(FSMNoteForm.note_hours), F.data.in_([i for i in dict_hours.keys()]))
    dp.message.register(warning_not_button,StateFilter(FSMNoteForm.note_hours))
    #ввод минуты
    dp.message.register(process_cur_minute,StateFilter(FSMNoteForm.note_minute), CheckForMinute())
    dp.message.register(warning_cur_minute,StateFilter(FSMNoteForm.note_minute))


    #удаление заметки и проверка, что больше одной заметки у человека
    dp.message.register(DelNote_handler, Command(commands='delnote'),StateFilter(default_state), CheckDatabaseMore())
    dp.message.register(process_note_del, StateFilter(FSMNoteDel.note_id))
    dp.message.register(warning_NoOne, Command(commands='delnote'),StateFilter(default_state))
    #вывод списка заметок у человека и проверка, что у него их больше одного
    dp.message.register(MyNotes_handler, Command(commands='mynotes'),StateFilter(default_state),CheckDatabaseMore())
    dp.message.register(warning_NoOne, Command(commands='mynotes'),StateFilter(default_state))
    #остановка всех активных уведомлений и проверка, что активных уведомленний больше одного
    dp.message.register(StopNotifications_handler, Command(commands='stopnotifications'),StateFilter(default_state),CheckNotifications())
    dp.message.register(warning_StopNotifications, Command(commands='stopnotifications'),StateFilter(default_state))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    Process(target=checktime).start()
    Process(target=notice).start()
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())