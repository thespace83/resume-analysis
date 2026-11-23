from aiogram.fsm.state import State, StatesGroup


class DeleteResumeState(StatesGroup):
    accept = State()
