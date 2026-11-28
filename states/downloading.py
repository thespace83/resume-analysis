from aiogram.fsm.state import State, StatesGroup


class DownloadingState(StatesGroup):
    downloading = State()
