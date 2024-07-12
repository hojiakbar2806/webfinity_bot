import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from bot import handlers
from bot.middlewares import LoggingMiddleware
from data.config import settings

ALLOWED_UPDATES = ["message", "edit_message"]

bot = Bot(settings.BOT_TOKEN)
dp = Dispatcher()

dp.message.middleware(LoggingMiddleware())


async def main():
    dp.include_router(handlers.cmd_router)
    dp.include_router(handlers.inline_router)
    dp.include_router(handlers.msg_router)
    dp.include_router(handlers.register_state_router)
    dp.include_router(handlers.sender_state_router)
    dp.include_router(handlers.timer_state_router)

    await dp.start_polling(bot)
    await bot.delete_my_commands()
    await bot.set_my_commands([
        BotCommand(command="start", description="Bot ni ishga tushirish"),
        BotCommand(command="register", description="Ro'xatdan o'tish"),
        BotCommand(command="my_info", description="Ma'lumotlaringizni ko'rish"),
        BotCommand(command="get_weather", description="Bugungi ob-havo ma'lumotlarini olish"),
        BotCommand(command="add_likee", description="Xabarga likee qadash"),
        BotCommand(command="play", description="O'yinni boshlash uchun"),
        BotCommand(command="top", description="Eng baland bal yig'gan o'yinchilar"),
        BotCommand(command="start_timer", description="Teskari sanash")
    ])


if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
