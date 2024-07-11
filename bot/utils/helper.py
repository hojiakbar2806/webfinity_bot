import os

from aiogram import Bot
from aiogram.filters.callback_data import CallbackData
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from geopy.geocoders import Nominatim


async def download_profile_pic(message, bot):
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    file_path = file_info.file_path
    os.makedirs('images', exist_ok=True)
    local_file_path = os.path.join(
        'images', f'{message.chat.id}_profile_pic.jpg')
    await bot.download_file(file_path, local_file_path)
    return local_file_path


async def delete_profile_pic(path):
    if path:
        if os.path.exists(path):
            os.remove(path)


async def can_delete_messages(chat_id: int, bot: Bot) -> bool:
    bot_id = (await bot.get_me()).id
    chat_member = await bot.get_chat_member(chat_id, bot_id)
    if chat_member.status in ('administrator', 'creator') and chat_member.can_delete_messages:
        return True
    return False


async def get_address_from_coordinates(latitude, longitude):
    geolocator = Nominatim(user_agent="geoapiExercises")

    try:
        location = geolocator.reverse((latitude, longitude), exactly_one=True)
        address = location.address
        return address
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        return f"Geocoding error: {e}"
    except Exception as e:
        return f"An error occurred: {e}"


class BallsCallbackFactory(CallbackData, prefix="ball"):
    color: str
