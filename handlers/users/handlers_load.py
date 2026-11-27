from __future__ import annotations

from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from repositories.resumes_repo import ResumesRepository
from states import LoadResumeState, MenuState
from utils.messages.menu import activate_main_menu
from utils.messages.messages_load import load_document, activate_load_document, start_load_documents

router = Router(name="users:load")


@router.message(MenuState.menu, F.text == "Загрузка")
async def load_handler(message: Message, state: FSMContext) -> None:
    await activate_load_document(message, state)


@router.message(LoadResumeState.waiting_for_document, F.text == "Отмена")
async def cancel_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await activate_main_menu(message, state, repo)


@router.message(LoadResumeState.waiting_for_document, F.document)
async def document_delivered_handler(
        message: Message,
        bot: Bot,
        state: FSMContext,
        repo: ResumesRepository,
        media_events: list[Message] = [],
) -> None:
    messages = media_events or [message]

    await start_load_documents(message, repo, state)
    for msg in messages:
        await load_document(bot, msg, repo)
