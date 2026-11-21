from __future__ import annotations

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from repositories.resumes_repo import ResumesRepository
from states import FiltersState
from utils.messages.select_filter import activate_name_filters
from utils.messages.find import activate_filters

router = Router(name="users:apply_filter")


@router.message(FiltersState.select_name, F.text == "Отмена")
async def cancel_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await activate_filters(message, state, repo)


@router.message(FiltersState.select_name, F.text)
async def name_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await activate_name_filters(message, state)
