from __future__ import annotations

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from models.resume import FilterTypes
from repositories.resumes_repo import ResumesRepository
from states import FiltersState
from utils.messages.apply_filter import apply_name_filters, reset_filters
from utils.messages.find import activate_filters

router = Router(name="users:apply_filter")


@router.message(FiltersState.select_name, F.text == "Отмена")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    await activate_filters(message, state)


@router.message(FiltersState.select_name, F.text == "Сбросить")
async def reset_handler(state: FSMContext) -> None:
    await reset_filters(state, FilterTypes.NAME)


@router.message(FiltersState.select_name, F.text)
async def name_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await apply_name_filters(message, state)
