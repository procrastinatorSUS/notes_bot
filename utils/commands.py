from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot:Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начало работы'
        ),
        BotCommand(
            command='help',
            description='список доступных команд'
        ),
        BotCommand(
            command='mynotes',
            description='мои активировнные заметки'
        ),
        BotCommand(
            command='addnote',
            description='добавить заметку'
        ),
        BotCommand(
            command='delnote',
            description='удалить заметку заметку'
        ),
        BotCommand(
            command='stopnotifications',
            description='отключить отправку сообщений'
        ),
        BotCommand(
            command='cancel',
            description='выйти из состояния закладок'
        )
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())