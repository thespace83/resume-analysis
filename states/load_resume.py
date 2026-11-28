from aiogram.fsm.state import State, StatesGroup


class LoadResumeState(StatesGroup):
    waiting_for_open_document = State()
    waiting_for_close_document = State()
