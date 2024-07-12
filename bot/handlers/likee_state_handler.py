import logging
from datetime import datetime

from aiogram import Router, types, Bot, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot import keyboards as kb
from bot.filters.admin import IsAdmin
from bot.states import LikeeState
from data.config import settings

likee_state_handler = Router()

GLOBAL_LIKES = 0
GLOBAL_DISLIKES = 0


@likee_state_handler.message(StateFilter(None), Command('add_likee'), IsAdmin())
async def post_channel(message: types.Message, state: FSMContext):
    await state.update_data(chat_id=message.chat.id)
    await message.answer("Post matnini, videosini yoki rasmini yuklang", reply_markup=kb.delete())
    await state.set_state(LikeeState.get_message)


@likee_state_handler.message(LikeeState.get_message, F.text)
async def get_message(message: types.Message, state: FSMContext):
    await state.update_data(message=message.text)
    await message.answer("Postingizga likee qo'shilsinmi", reply_markup=kb.confirm())
    await state.set_state(LikeeState.confirm_likee)


@likee_state_handler.message(LikeeState.get_message, F.photo)
async def get_message(message: types.Message, state: FSMContext):
    await state.update_data(photo_id=message.photo[-1].file_id, caption=message.caption)
    await message.answer("Postingizga likee qo'shilsinmi", reply_markup=kb.confirm())
    await state.set_state(LikeeState.confirm_likee)


@likee_state_handler.message(LikeeState.get_message, F.video)
async def get_message(message: types.Message, state: FSMContext):
    await state.update_data(video_id=message.video.file_id, caption=message.caption)
    await message.answer("Postingizga likee qo'shilsinmi", reply_markup=kb.confirm())
    await state.set_state(LikeeState.confirm_likee)


@likee_state_handler.message(LikeeState.confirm_likee, lambda message: message.text in ["Ha", "Yo'q"])
async def confirm_and_send(message: types.Message, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    channel_id = settings.CHANNEL_ID

    photo_id = user_data.get("photo_id")
    video_id = user_data.get("video_id")
    caption = user_data.get("caption")

    if message.text == "Ha":
        if photo_id:
            await bot.send_photo(chat_id=channel_id, photo=photo_id, caption=caption, reply_markup=kb.likee(0, 0))
        if video_id:
            await bot.send_video(chat_id=channel_id, video=video_id, caption=caption, reply_markup=kb.likee(0, 0))
        if user_data.get("message"):
            await bot.send_message(text=user_data.get("message"), chat_id=channel_id, reply_markup=kb.likee(0, 0))
    elif message.text == "Yo'q":
        if photo_id:
            await bot.send_photo(chat_id=channel_id, photo=photo_id, caption=caption, reply_markup=kb.delete())
        if video_id:
            await bot.send_video(chat_id=channel_id, video=video_id, caption=caption, reply_markup=kb.delete())
        if user_data.get("message"):
            await bot.send_message(text=user_data.get("message"), chat_id=channel_id, reply_markup=kb.delete())
        await bot.send_message(text="Xabaringiz jo'natildi", chat_id=channel_id, reply_markup=kb.delete())
    await message.reply(text="Amaliyot bajarildi", reply_markup=kb.delete())
    await state.clear()


@likee_state_handler.callback_query(lambda query: query.data.startswith('action'))
async def likee_query(query: CallbackQuery, bot: Bot, state: FSMContext):
    global GLOBAL_LIKES, GLOBAL_DISLIKES

    user_data = await state.get_data()
    user_id = query.from_user.id
    username = query.from_user.username
    message_id = query.message.message_id
    action = query.data[7:]

    try:
        if user_id not in user_data:
            user_data[user_id] = {}

        if message_id not in user_data[user_id]:
            user_data[user_id][message_id] = {
                'is_like': None,
                'action_time': str(datetime.now()),
            }

        if user_data[user_id][message_id]["is_like"] == True and action == 'like':
            await query.answer("Siz allaqachon like bosgansiz")
            return

        if user_data[user_id][message_id]["is_like"] == False and action == 'dislike':
            await query.answer("Siz allaqachon dislike bosgansiz")
            return

        if action == "like":
            if user_data[user_id][message_id]["is_like"] is None or user_data[user_id][message_id]["is_like"] is False:
                GLOBAL_LIKES += 1
                if user_data[user_id][message_id]["is_like"] is False:
                    GLOBAL_DISLIKES -= 1
                user_data[user_id][message_id]["is_like"] = True

        elif action == "dislike":
            if user_data[user_id][message_id]["is_like"] is None or user_data[user_id][message_id]["is_like"] is True:
                GLOBAL_DISLIKES += 1
                if user_data[user_id][message_id]["is_like"] is True:
                    GLOBAL_LIKES -= 1
                user_data[user_id][message_id]["is_like"] = False

        await state.update_data(user_data)
        logging.info(
            f"User @{username} {action}d message {message_id} at {str(datetime.now())}"
        )

        await bot.edit_message_reply_markup(
            chat_id=query.message.chat.id,
            message_id=message_id,
            reply_markup=kb.likee(GLOBAL_LIKES, GLOBAL_DISLIKES)
        )
    except Exception as e:
        logging.error(f"Error handling @{username}'s action: {e}")
        try:
            await query.answer("Xatolik yuz berdi, iltimos qayta urinib ko'ring.")
        except TelegramBadRequest as ex:
            logging.error(f"Failed to send answer: {ex}")
