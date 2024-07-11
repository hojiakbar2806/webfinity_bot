import logging
from contextlib import suppress

from aiogram import Router, Bot, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy import select

from bot import keyboards as kb
from bot.services.likee_service import like_service
from bot.utils import BallsCallbackFactory
from data.base import get_session
from data.config import settings
from data.crud import get_user_by_chat_id
from data.models.gamer import GamerScore

inline_router = Router()


# noinspection PyBroadException
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

    session.delete(user)
    session.commit()
    await query.message.delete()
    await query.answer("Malumotlar o'chirildi", show_alert=True)


@inline_router.callback_query(lambda query: query.data.startswith('action_'))
async def handle_action_query(query: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        values = await like_service(query, state)
        print(values)
        await bot.edit_message_reply_markup(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id,
            reply_markup=kb.likee(values["likes"], values["dislikes"])
        )
    #
    except Exception as e:
        logging.error(f"Error occurred while handling action query: {str(e)}")
        await query.answer("Xatolik yuz berdi, iltimos qayta urinib ko'ring.")


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
