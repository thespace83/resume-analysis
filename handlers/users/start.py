"""Handles the /start command."""
from __future__ import annotations

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.default import get_menu_keyboard

router = Router(name="users:start")


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(
        f'Аналитика Резюме\n\n'
        "Чтобы загрузить резюме используйте \"Загрузка\"\n"
        "Чтобы найти резюме используйте \"Поиск\"\n",
        reply_markup=get_menu_keyboard(),
    )
