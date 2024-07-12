import asyncio
import logging
from contextlib import suppress

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery
from sqlalchemy import select

from bot import keyboards as kb
from bot.utils import BallsCallbackFactory
from data.base import get_session
from data.config import settings
from data.crud import get_user_by_chat_id, promote_to_admin
from data.models.gamer import GamerScore

inline_router = Router()


@inline_router.callback_query(lambda query: query.data == "check_subscriber")
async def check_subscriber_handler(callback_query: CallbackQuery):
    """
    :param callback_query:
    """
    bot = callback_query.bot
    member = await bot.get_chat_member(chat_id=settings.CHANNEL_ID, user_id=callback_query.from_user.id)

    if member.status in ["owner", "member", "creator"]:
        await callback_query.answer("Ok, Endi davom etishingiz mumkin")
        try:
            await bot.delete_message(chat_id=callback_query.message.chat.id,
                                     message_id=callback_query.message.message_id)
        except Exception as e:
            logging.error(f"Xabarni o'chirishda xatolik: {e}")
    else:
        await callback_query.answer("Kanallarga a'zo bo'lib qayta urinib ko'ring")


@inline_router.callback_query(lambda query: query.data == "delete_user_info")
async def delete_user_info(query: CallbackQuery):
    chat_id = query.from_user.id

    async with get_session() as session:
        user = await get_user_by_chat_id(session, chat_id)

    if not user:
        await query.answer("Foydalanuvchi topilmadi", show_alert=True)
        await query.message.delete()
        return

    await session.delete(user)
    await session.commit()
    await query.answer("Malumotlar o'chirildi")
    await query.message.delete()


@inline_router.callback_query(BallsCallbackFactory.filter(F.color == "red"))
async def cb_miss(callback: CallbackQuery):
    async with get_session() as session:
        await session.merge(GamerScore(user_id=callback.from_user.id, score=0))
        await session.commit()

    with suppress(TelegramBadRequest):
        await callback.message.edit_text("Your score: 0", reply_markup=kb.generate_balls())


@inline_router.callback_query(BallsCallbackFactory.filter(F.color == "green"))
async def cb_hit(callback: CallbackQuery):
    async with get_session() as session:
        db_query = await session.execute(select(GamerScore).filter_by(user_id=callback.from_user.id))
        player: GamerScore = db_query.scalar()
        # Note: we're incrementing client-side, not server-side
        player.score += 1
        await session.commit()

    # Since we have "expire_on_commit=False", we can use player instance here
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(f"Your score: {player.score}", reply_markup=kb.generate_balls())


@inline_router.callback_query(lambda c: c.data.startswith('start_timer'))
async def start_timer(callback_query: CallbackQuery):
    countdown_seconds = int(callback_query.data.split(':')[1])
    message = callback_query.message
    for i in range(countdown_seconds, 0, -1):
        await message.edit_text(f"Qolgan vaqt: {i} sekund")
        await asyncio.sleep(1)
    await message.edit_text("Vaqt tugadi!")


@inline_router.callback_query(lambda query: query.data.startswith('promote_admin'))
async def promote_admin_callback_handler(query: CallbackQuery):
    try:
        chat_id = int(query.data.split(':')[-1])
        success = await promote_to_admin(chat_id)
        if success:
            await query.answer("Foydalanuvchi muvaffaqiyatli admin deb belgilandi")
        else:
            await query.answer("Foydalanuvchi topilmadi yoki allaqachon admin", show_alert=True)
    except Exception as e:
        await query.answer("An error occurred while processing your request.", show_alert=True)
        print(f"Error promoting user: {e}")
