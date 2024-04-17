from aiogram.types import Message
from aiogram.filters import BaseFilter
import aiosqlite as sq
class CheckDatabaseLess(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        async with sq.connect('users.db') as db:
            cursor = await db.execute(f"SELECT COUNT(*) FROM notes WHERE user_id = {message.from_user.id}")
            check = await cursor.fetchone()
            if check[0] < 10:
                return True
            else:
                return False
            
class CheckDatabaseMore(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        async with sq.connect('users.db') as db:
            cursor = await db.execute(f"SELECT COUNT(*) FROM notes WHERE user_id = {message.from_user.id}")
            check = await cursor.fetchone()
            if check[0] >= 1:
                return True
            else:
                return False

class CheckNotifications(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        async with sq.connect('users.db') as db:
            cursor = await db.execute(f"SELECT COUNT(*) FROM notifications WHERE user_id = {message.from_user.id}")
            check = await cursor.fetchone()
            if check[0] >= 1:
                return True
            else:
                return False
            
class CheckForMinute(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.text.isdigit() and (len(message.text) == 1 or len(message.text) == 2) and int(message.text) <= 59:
            return True
        else:
            return False