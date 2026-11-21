from __future__ import annotations

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from repositories.resumes_repo import ResumesRepository
from states import FiltersState
from utils.messages.select_filter import activate_name_filters
from utils.messages.find import activate_find_document

router = Router(name="users:select_filter")


@router.message(FiltersState.select_filter, F.text == "Имя")
async def name_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await activate_name_filters(message, state)


@router.message(FiltersState.select_filter, F.text == "Отмена")
async def cancel_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await activate_find_document(message, state, repo)
