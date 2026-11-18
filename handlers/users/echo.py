"""Echoes any text message back to the sender."""
from __future__ import annotations

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router(name="users:echo")


# @router.message(F.text)
# async def echo_handler(message: Message, state: FSMContext) -> None:
#     await message.answer(message.text)
