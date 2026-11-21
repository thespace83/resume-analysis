from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from models.resume import FilterTypes
from repositories.resumes_repo import ResumesRepository
from states import FiltersState
from utils.messages.find import activate_find_document


async def apply_filter(
        message: Message,
        state: FSMContext,
        repo: ResumesRepository,
        target: FilterTypes
) -> None:
    if message.text is None:
        return
    if target == FilterTypes.NAME:
        await state.update_data(name=message.text)
    elif target == FilterTypes.PROFESSION:
        await state.update_data(profession=message.text)
    elif target == FilterTypes.INFO:
        await state.update_data(info=message.text)

    await state.set_state(FiltersState.select_filter)
    await activate_find_document(message, state, repo)


async def reset_filters(
        message: Message,
        state: FSMContext,
        repo: ResumesRepository,
        filter_type: FilterTypes
) -> None:
    if filter_type == FilterTypes.NAME:
        await state.update_data(name=None)
    elif filter_type == FilterTypes.PROFESSION:
        await state.update_data(profession=None)
    elif filter_type == FilterTypes.INFO:
        await state.update_data(info=None)
    await activate_find_document(message, state, repo)
