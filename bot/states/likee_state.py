from aiogram.fsm.state import State, StatesGroup


class LikeeState(StatesGroup):
    get_message = State()
    confirm_likee = State()
