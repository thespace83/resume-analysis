from __future__ import annotations

from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from repositories.resumes_repo import ResumesRepository
from states import LoadResumeState, MenuState
from utils.messages.menu import activate_main_menu
from utils.messages.load_document import load_open_document, activate_load_open_document, start_load_documents, \
    load_closed_document, activate_load_closed_document

router = Router(name="users:load")


@router.message(MenuState.menu, F.text == "Загрузка Открытого")
async def load_open_document_handler(message: Message, state: FSMContext) -> None:
    await activate_load_open_document(message, state)


@router.message(MenuState.menu, F.text == "Загрузка Закрытого")
async def load_close_document_handler(message: Message, state: FSMContext) -> None:
    await activate_load_closed_document(message, state)


@router.message(LoadResumeState.waiting_for_open_document, F.text == "Отмена")
async def cancel_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await activate_main_menu(message, state, repo)


@router.message(LoadResumeState.waiting_for_open_document, F.document)
async def open_document_delivered_handler(
        message: Message,
        bot: Bot,
        state: FSMContext,
        repo: ResumesRepository,
        media_events: list[Message] = [],
) -> None:
    messages = media_events or [message]

    await start_load_documents(message, repo, state)
    for msg in messages:
        await load_open_document(bot, msg, repo)


@router.message(LoadResumeState.waiting_for_close_document, F.document)
async def closed_document_delivered_handler(
        message: Message,
        bot: Bot,
        state: FSMContext,
        repo: ResumesRepository,
) -> None:
    await load_closed_document(bot, state, message, repo)
