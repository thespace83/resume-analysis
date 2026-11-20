from __future__ import annotations

import asyncio
import logging
import os
from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, Document, ReplyKeyboardMarkup
from utils.resume import publish_document

from states import LoadResumeState, MenuState

from keyboards.default import get_cancel_keyboard, get_menu_keyboard

router = Router(name="users:load")


@router.message(F.text == "Загрузка")
async def load_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(LoadResumeState.waiting_for_document)
    await message.answer(
        f"Загрузите документ\n\nДоступные форматы: pdf",
        reply_markup=get_cancel_keyboard()
    )


@router.message(LoadResumeState.waiting_for_document, F.document)
async def document_delivered_handler(message: Message, bot: Bot, state: FSMContext) -> None:
    if message.document is None:
        logging.error("The document has not been delivered.")
        return
    document = message.document

    if not is_pdf(document.file_name):
        await message.answer(f"Формат \".{document.file_name.split(".")[-1:][0]}\" не поддерживается")
        return
    if not has_correct_size(document.file_size):
        await message.answer(f"Файл весит больше лимита в 20 MB")
        return

    await state.set_state(MenuState.menu)
    await message.answer(f"Вы можете продолжать работу\n\nДокумент загружается и будет доступен через некоторое время",
                         reply_markup=get_menu_keyboard())

    await asyncio.to_thread(publish_document, bot, document)


def is_pdf(file_name: str | None) -> bool:
    return (file_name is not None) and (file_name.split(".")[-1:][0] == "pdf")


def has_correct_size(file_size: int | None) -> bool:
    return (file_size is not None) and (file_size > 20 * 1024 * 1024)
