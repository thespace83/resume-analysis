from __future__ import annotations

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from repositories.resumes_repo import ResumesRepository
from states import MenuState
from states.find_resume import FindResumeState
from utils.messages.find import activate_find_document, examine_file, activate_filters
from utils.messages.menu import activate_main_menu

router = Router(name="users:find")


@router.message(MenuState.menu, F.text == "Поиск")
async def find_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await activate_find_document(message, state, repo)


@router.message(FindResumeState.watching, F.text == "Обновить")
async def update_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await activate_find_document(message, state, repo)


@router.message(FindResumeState.watching, F.text == "Отмена")
async def cancel_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await activate_main_menu(message, state, repo)


@router.message(FindResumeState.watching, F.text == "Фильтры")
async def update_handler(message: Message, state: FSMContext) -> None:
    await activate_filters(message, state)


@router.message(FindResumeState.watching, F.text)
async def file_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await examine_file(message, state, repo)


@router.message(FindResumeState.watching_target, F.text == "Назад")
async def file_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await activate_find_document(message, state, repo)
