"""Handles the /help command."""
from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.default import get_help_keyboard

router = Router(name="users:help")


@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    await message.answer(
        "<b>Анализатор резюме</b>\n"
        "/start — чтобы начать работу\n"
        "/help — для вывода этого сообщения.",
        reply_markup=get_help_keyboard(),
    )
