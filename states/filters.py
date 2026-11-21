from aiogram.fsm.state import State, StatesGroup


class FiltersState(StatesGroup):
    select_filter = State()
