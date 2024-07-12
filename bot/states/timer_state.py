from aiogram.fsm.state import State, StatesGroup


class TimerState(StatesGroup):
    get_time = State()
    start_counter = State()
    stop = State()
