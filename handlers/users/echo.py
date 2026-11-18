"""Echoes any text message back to the sender."""
from __future__ import annotations

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states import MenuState, LoadResumeState

router = Router(name="users:echo")


@router.message(MenuState.menu, F.text)
async def echo_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Неизвестная команда\n\n" +
                         "Используйте \"Загрузка\" для загрузки резюме или \"Поиск\" для поиска по доступным резюме")


@router.message(LoadResumeState.waiting_for_document, F.text)
async def echo_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Загрузите документ или используйте \"Отмена\"")
