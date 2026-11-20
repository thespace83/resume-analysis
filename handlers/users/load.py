from __future__ import annotations

import aiomysql
from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states import LoadResumeState, MenuState
from utils.messages.load import load_document, activate_load_document
from utils.messages.menu import activate_main_menu

router = Router(name="users:load")


@router.message(MenuState.menu, F.text == "Загрузка")
async def load_handler(message: Message, state: FSMContext) -> None:
    await activate_load_document(message, state)


@router.message(LoadResumeState.waiting_for_document, F.text == "Отмена")
async def cancel_handler(message: Message, state: FSMContext, conn: aiomysql.Connection) -> None:
    await activate_main_menu(message, state, conn)


@router.message(LoadResumeState.waiting_for_document, F.document)
async def document_delivered_handler(message: Message, bot: Bot, state: FSMContext, conn: aiomysql.Connection) -> None:
    await load_document(bot, message, state, conn)
