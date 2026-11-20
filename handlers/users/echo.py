"""Echoes any text message back to the sender."""
from __future__ import annotations

from aiogram import F, Router
from aiogram.types import Message

from states import LoadResumeState

router = Router(name="users:echo")


@router.message(LoadResumeState.waiting_for_document, F.text)
async def load_echo_handler(message: Message) -> None:
    await message.answer("Загрузите документ или используйте \"Отмена\"")
