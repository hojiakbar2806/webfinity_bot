import asyncio

from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot import keyboards as kb
from bot.states import TimerState

timer_state_router = Router()


@timer_state_router.message(StateFilter(TimerState.get_time))
async def get_time(message: types.Message, state: FSMContext):
    try:
        time = int(message.text)
        await state.update_data(time=time)
        await state.set_state(TimerState.start_counter)
        await message.reply("Boshlashga tayyor bo'lsangiz tugmani bosing", reply_markup=kb.start_counter())
    except ValueError:
        await message.reply("Iltimos, faqat raqam kiriting.")


@timer_state_router.message(StateFilter(TimerState.start_counter), F.text == "Boshlash")
async def start_timer(message: types.Message, state: FSMContext):
    count_data = await state.get_data()
    countdown_seconds = count_data.get("time", 0)
    msg = await message.answer(f"Sanoq boshlandi", reply_markup=kb.stop_counter())
    await state.set_state(TimerState.stop)
    for i in range(countdown_seconds, 0, -1):
        if count_data.get('stop_requested'):
            return
        await asyncio.sleep(1)
        await msg.edit_text(f"Qolgan vaqt: {i} sekund", reply_markup=kb.stop_counter())

    await msg.edit_text("Vaqt tugadi!")
    await msg.answer(text="/start_timer", reply_markup=kb.delete())
    await state.clear()


@timer_state_router.callback_query(lambda query: query.data == "stop_timer", StateFilter(TimerState.stop))
async def stop_timer_callback(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text(f"Vaqt to'xtatildi.", reply_markup=None)
    await state.update_data(stop_requested=True)
    await state.clear()
