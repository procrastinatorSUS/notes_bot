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
            description='список записей'
        ),
        BotCommand(
            command='addnote',
            description='добавить заметку'
        ),
        BotCommand(
            command='delnote',
            description='удалить заметку'
        ),
        BotCommand(
            command='stopnotifications',
            description='остановить отправку сообщений'
        ),
        BotCommand(
            command='cancel',
            description='прекратить заполнять заметку'
        )
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())