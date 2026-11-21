from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from models.resume import FilterTypes
from repositories.resumes_repo import ResumesRepository
from states import FiltersState
from utils.messages.find import activate_filters, activate_find_document


async def apply_name_filters(
        message: Message,
        state: FSMContext,
        repo: ResumesRepository
) -> None:
    if message.text is None:
        return
    await state.update_data(name=message.text)
    await state.set_state(FiltersState.select_filter)
    await message.answer(f"Добавлен фильтр \"{await state.get_value("name")}\" для имени кандидата")
    await activate_find_document(message, state, repo)


async def reset_filters(
        message: Message,
        state: FSMContext,
        repo: ResumesRepository,
        filter_type: FilterTypes
) -> None:
    if filter_type == FilterTypes.NAME:
        await state.update_data(name=None)
        await activate_find_document(message, state, repo)
