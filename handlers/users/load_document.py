"""Handles the load document
"""
from __future__ import annotations

from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from repositories.resumes_repo import ResumesRepository
from states import LoadResumeState, MenuState
from utils.messages.load import load_document, activate_load_document
from utils.messages.menu import activate_main_menu

router = Router(name="users:load_document")


@router.message(MenuState.menu, F.text == "Загрузка")
async def menu_handler(message: Message, state: FSMContext) -> None:
    await activate_load_document(message, state)


@router.message(LoadResumeState.waiting_for_document, F.text == "Отмена")
async def cancel_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await activate_main_menu(message, state, repo)


@router.message(LoadResumeState.waiting_for_document, F.document)
async def load_document_handler(message: Message, bot: Bot, state: FSMContext, repo: ResumesRepository) -> None:
    await load_document(bot, message, state, repo)
