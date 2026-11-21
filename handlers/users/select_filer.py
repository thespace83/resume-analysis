from __future__ import annotations

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from repositories.resumes_repo import ResumesRepository
from states import FiltersState
from utils.messages.select_filter import activate_filter
from utils.messages.find import activate_find_document, activate_filters

router = Router(name="users:select_filter")

TYPES: dict[str, FiltersState] = {
    "Имя": FiltersState.select_name,
    "Профессия": FiltersState.select_profession,
    "Доп. информация": FiltersState.select_info,
    "Гендер": FiltersState.select_gender,
}


@router.message(FiltersState.select_filter)
async def name_handler(message: Message, state: FSMContext) -> None:
    text = message.text
    if text is None:
        await activate_filters(message, state)
        return
    if text not in TYPES:
        await activate_filters(message, state)
        return
    await activate_filter(message, state, TYPES[text])


@router.message(FiltersState.select_filter, F.text == "Отмена")
async def cancel_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await activate_find_document(message, state, repo)
