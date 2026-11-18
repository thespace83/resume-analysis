from aiogram.fsm.state import State, StatesGroup


class LoadResumeState(StatesGroup):
    waiting_for_document = State()
