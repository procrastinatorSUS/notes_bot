from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext
from main import FSMNoteForm, FSMNoteDel
from utils.generator_buttons import *
import aiosqlite as sq
from aiogram import Bot
user_dict: dict[int, dict[str, str | int | bool]] = {}
