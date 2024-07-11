import logging
from logging.handlers import RotatingFileHandler
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram import types

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('bot.log', maxBytes=1000000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        message = event if isinstance(event, types.Message) else None
        if message:
            user = message.from_user
            content = message.text or message.caption or "No text"
            log_data = {
                'username': user.username,
                'user_id': user.id,
                'chat_id': message.chat.id,
                'message_id': message.message_id,
                'content': content
            }
            if message.location:
                log_data.update({
                    'latitude': message.location.latitude,
                    'longitude': message.location.longitude
                })
            if message.photo:
                log_data.update({
                    'photo_ids': [photo.file_id for photo in message.photo]
                })

            logger.info(f"User: {log_data}")
        return await handler(event, data)
