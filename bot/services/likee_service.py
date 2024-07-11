# services.py
import logging
from datetime import datetime

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

GLOBAL_LIKES = 0
GLOBAL_DISLIKES = 0

LIKE_ACTION = 'like'
DISLIKE_ACTION = 'dislike'


async def like_service(query: CallbackQuery, state: FSMContext):
    global GLOBAL_LIKES, GLOBAL_DISLIKES

    user_data = await state.get_data()
    user_id = query.from_user.id
    username = query.from_user.username
    message_id = query.message.message_id
    action = query.data[7:]

    if user_id not in user_data:
        user_data[user_id] = {}

    if message_id not in user_data[user_id]:
        user_data[user_id][message_id] = {
            'is_like': None,
            'liked_at': str(datetime.now()),
            'username': username
        }

    if user_data[user_id][message_id]["is_like"] == True and action == 'like':
        await query.answer("Siz allaqachon like bosgansiz")
        return

    if user_data[user_id][message_id]["is_like"] == False and action == 'dislike':
        await query.answer("Siz allaqachon dislike bosgansiz")
        return

    if action == "like":
        if user_data[user_id][message_id]["is_like"] is None or user_data[user_id][message_id][
            "is_like"] is False:
            GLOBAL_LIKES += 1
            if user_data[user_id][message_id]["is_like"] is False:
                GLOBAL_DISLIKES -= 1
            user_data[user_id][message_id]["is_like"] = True

    elif action == "dislike":
        if user_data[user_id][message_id]["is_like"] is None or user_data[user_id][message_id][
            "is_like"] is True:
            GLOBAL_DISLIKES += 1
            if user_data[user_id][message_id]["is_like"] is True:
                GLOBAL_LIKES -= 1
            user_data[user_id][message_id]["is_like"] = False

    await state.update_data(user_data)
    logging.info(f"User @{username} {action}d message {message_id} at {str(datetime.now())}")

    return {"likes": GLOBAL_LIKES, "dislikes": GLOBAL_DISLIKES}
