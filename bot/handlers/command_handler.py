from aiogram import types, html, Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from sqlalchemy import select

from bot import keyboards as kb
from bot.filters import IsSubscriber
from bot.states import WeatherState, RegisterState, TimerState
from bot.utils import get_address_from_coordinates
from data.base import get_session
from data.crud import get_user_by_chat_id
from data.models.gamer import GamerScore

cmd_router = Router()


@cmd_router.message(Command('start'))
async def start_handler(message: types.Message, bot: Bot):
    pass


@cmd_router.message(StateFilter(None), Command('get_weather'), IsSubscriber())
async def weather_handler(message: types.Message, state: FSMContext, bot: Bot):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    await message.answer("Manzilingizni ulashing", reply_markup=kb.location())
    await state.set_state(WeatherState.send_weather)


@cmd_router.message(StateFilter(None), Command("register"))
async def register_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    async with get_session() as session:
        user = await get_user_by_chat_id(session, chat_id)
        if user:
            await message.answer("Siz allaqachon ro'yxatdan o'tganziz")
            return
        await message.answer("Ismingizni kiriting")
        await state.update_data(chat_id=message.from_user.id)
        await state.set_state(RegisterState.first_name)


@cmd_router.message(Command('my_info'))
async def get_user_info(message: types.Message, bot: Bot):
    chat_id = message.chat.id
    text = "Iltimos ro'yxatdan o'ting. Buning uchun /register buyrug'ini kiriting"

    async with get_session() as session:
        user = await get_user_by_chat_id(session, chat_id)

    if not user:
        return await message.answer(text, reply_markup=kb.delete())
    if user.latitude and user.longitude:
        address = await get_address_from_coordinates(user.latitude, user.longitude)
    address = "Kiritilmagan"

    info_message = (
        f"Your Info: \n"
        f"Ism: {user.first_name}\n"
        f"Familya: {user.last_name}\n"
        f"Telefon no'mer: {user.phone_number}\n"
        f"Jins: {user.gender}\n"
        f"Manzil: {address}"
    )

    if user.profile_pic:
        photo_data = FSInputFile(path=user.profile_pic)
        await bot.send_photo(chat_id, photo=photo_data, caption=info_message, reply_markup=kb.delete_user())

    else:
        await message.answer(info_message, reply_markup=kb.delete_user())


@cmd_router.message(Command("play"))
async def cmd_play(message: types.Message):
    async with get_session() as session:
        await session.merge(GamerScore(user_id=message.from_user.id, score=0))
        await session.commit()

    await message.answer("Your score: 0", reply_markup=kb.generate_balls())


@cmd_router.message(Command("top"))
async def cmd_top(message: types.Message):
    async with get_session() as session:
        sql = select(GamerScore).order_by(GamerScore.score.desc()).limit(5)
        text_template = "Top 5 players:\n\n{scores}"
        top_players_request = await session.execute(sql)
        players = top_players_request.scalars()

    score_entries = [f"{index + 1}. ID{item.user_id}: {html.bold(item.score)}" for index, item in enumerate(players)]
    score_entries_text = "\n".join(score_entries) \
        .replace(f"{message.from_user.id}", f"{message.from_user.id} (it's you!)")
    await message.answer(text_template.format(scores=score_entries_text), parse_mode="HTML")


@cmd_router.message(StateFilter(None), Command('start_timer'))
async def start_timer(message: types.Message, state: FSMContext):
    await message.reply("Vaqt kiriting kirting faqat soniyada", reply_markup=kb.delete())
    await state.set_state(TimerState.get_time)
