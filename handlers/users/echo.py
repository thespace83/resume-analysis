"""Echoes any text message back to the sender."""
from __future__ import annotations

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from repositories.resumes_repo import ResumesRepository
from states import MenuState, LoadResumeState

from utils.messages.menu import activate_main_menu

router = Router(name="users:echo")


@router.message(LoadResumeState.waiting_for_document, F.text)
async def load_echo_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Загрузите документ или используйте \"Отмена\"")


@router.message()
async def no_state_echo_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await activate_main_menu(message, state, repo)
