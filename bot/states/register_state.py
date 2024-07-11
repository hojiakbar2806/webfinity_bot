from aiogram.fsm.state import State, StatesGroup


class RegisterState(StatesGroup):
    first_name = State()
    last_name = State()
    phone_number = State()
    gender = State()
    location = State()
    profile_pic = State()
    confirmation = State()
