"""Handles the /start command."""
from __future__ import annotations

import aiomysql
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from utils.messages.menu import activate_main_menu

router = Router(name="users:start")


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext, conn: aiomysql.Connection) -> None:
    await activate_main_menu(message, state, conn)
