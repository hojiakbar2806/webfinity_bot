from aiogram.fsm.state import State, StatesGroup


class WeatherState(StatesGroup):
    send_weather = State()
