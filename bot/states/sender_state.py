from aiogram.fsm.state import State, StatesGroup


class SenderState(StatesGroup):
    get_message = State()
    confirm_likee = State()