from All_imports_For_Project.import_lib import *

#Отвечает на ввод команды /start
async def start_handler(message: Message, bot:Bot):
    await message.answer("Привет! данный бот позволит тебе создать заметку.\nДобавить заметку по команде /addnote\nДоступно до 10 активных заметок.\nКоманда /help покажет возможности бота.")


#Отвечает на ввод команды /help
async def help_command(message:Message):
    await message.answer('Список доступных команд:\n/addnote — добавить заметку\n/mynotes — выводит список ваших заметок\n/delnote — по выбору удаляет оставленную заметку\n/stopnotifications — останавливает отправку уведомлений\n/cancel — отменяет процесс создания заметки и её удаления')
