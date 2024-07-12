from aiogram import types, Router, Bot, F
from aiogram.fsm.context import FSMContext

from bot import keyboards as kb
from bot.filters import IsSubscriber
from bot.services import fetch_weather_data, weather_info
from bot.states import WeatherState

msg_router = Router()


@msg_router.message(WeatherState.send_weather, F.location, IsSubscriber())
async def send_weather(message: types.Message, state: FSMContext, bot: Bot):
    username = message.from_user.username
    chat_id = message.chat.id
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    c_msg = await bot.send_message(chat_id, text="⌛️")
    lat = message.location.latitude
    lon = message.location.longitude
    data = await fetch_weather_data(lat, lon, username)
    info = await weather_info(data)
    await bot.delete_message(chat_id, message_id=c_msg.message_id)
    await message.answer(info, reply_markup=kb.delete())
    await state.clear()
