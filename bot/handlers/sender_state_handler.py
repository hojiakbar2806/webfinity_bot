from aiogram import Bot, F
from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from bot import keyboards as kb
from bot.filters import ChatTypeFilter
from bot.states import SenderState
from data.config import settings

sender_state_router = Router()


@sender_state_router.message(SenderState.get_message, F.text)
async def get_message(message: types.Message, state: FSMContext):
    await state.update_data(message=message.text)
    await message.answer("Postingizga likee qo'shilsinmi", reply_markup=kb.confirm())
    await state.set_state(SenderState.confirm_likee)


@sender_state_router.message(SenderState.get_message, F.photo)
async def get_message(message: types.Message, state: FSMContext):
    await state.update_data(photo_id=message.photo[-1].file_id, caption=message.caption)
    await message.answer("Postingizga likee qo'shilsinmi", reply_markup=kb.confirm())
    await state.set_state(SenderState.confirm_likee)


@sender_state_router.message(SenderState.get_message, F.video)
async def get_message(message: types.Message, state: FSMContext):
    await state.update_data(video_id=message.video.file_id, caption=message.caption)
    await message.answer("Postingizga likee qo'shilsinmi", reply_markup=kb.confirm())
    await state.set_state(SenderState.confirm_likee)


@sender_state_router.message(SenderState.confirm_likee, lambda message: message.text in ["Ha", "Yo'q"])
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
