from __future__ import annotations

import logging
import os
from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, Document

from states import LoadResumeState, MenuState

router = Router(name="users:load")


@router.message(F.text == "Загрузка")
async def load_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(LoadResumeState.waiting_for_document)
    await message.answer(f"Загрузите документ\n\nДоступные форматы: pdf")


@router.message(LoadResumeState.waiting_for_document, F.document)
async def document_delivered_handler(message: Message, bot: Bot, state: FSMContext) -> None:
    if message.document is None:
        logging.error("The document has not been delivered.")
    document = message.document

    if document.file_name.split(".")[-1:][0] != "pdf":
        await message.answer(f"Формат \".{document.file_name.split(".")[-1:][0]}\" не поддерживается")
        return
    if document.file_size > 20 * 1024 * 1024:
        await message.answer(f"Файл весит больше лимита в 20 MB")
        return

    await state.set_state(MenuState.menu)
    await message.answer(f"Документ загружается и будет доступен через некоторое время\nВы можете продолжать работу")
    await bot.download(document, destination=os.path.join(os.getcwd(), "documents", f"{document.file_id}.pdf"))
    logging.info("File is downloaded")
