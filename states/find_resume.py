from aiogram.fsm.state import State, StatesGroup


class FindResumeState(StatesGroup):
    watching = State()
    waiting_for_filters = State()
