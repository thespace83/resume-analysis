"""Handles the /start command."""
from __future__ import annotations

import aiomysql
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states import MenuState

from keyboards.default import get_menu_keyboard

router = Router(name="users:start")


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext, conn: aiomysql.Connection) -> None:
    await state.set_state(MenuState.menu)
    await message.answer(
        f'Аналитика Резюме\n\n'
        "Чтобы загрузить резюме используйте \"Загрузка\"\n"
        "Чтобы найти резюме используйте \"Поиск\"\n",
        reply_markup=get_menu_keyboard(),
    )

    async with conn.cursor() as cur:
        await cur.execute("SELECT COUNT(*) FROM resumes")
        count = (await cur.fetchone())[0]
    await message.answer(f"Всего пользователей: {count}")
