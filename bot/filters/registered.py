from aiogram.filters import Filter
from aiogram import types, Bot
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from data.base import get_session
from data.models import User
from bot import keyboards as kb


class IsRegistered(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        chat_id = message.chat.id
        text = "Iltimos ro'yxatdan o'ting. Buning uchun /register buyrug'ini kiriting"

        async with get_session() as session:
            async with session.begin():
                query = select(User).filter(User.chat_id == chat_id)
                user = await session.execute(query).result.first()
                if not user:
                    await message.answer(text, reply_markup=kb.delete())
                    return False
                return True
