from __future__ import annotations

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from repositories.resumes_repo import ResumesRepository
from states import MenuState, DeleteResumeState
from states.find_resume import FindResumeState
from utils.messages.delete import activate_delete_menu, delete_document
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
async def examine_file_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await examine_file(message, state, repo)


@router.message(FindResumeState.watching_target, F.text == "Назад")
async def back_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await activate_find_document(message, state, repo)


@router.message(FindResumeState.watching_target, F.text == "Удалить")
async def delete_document_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await activate_delete_menu(message, state, repo)


@router.message(DeleteResumeState.accept, F.text == "Нет, не удалять")
async def cancel_delete_document_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await activate_find_document(message, state, repo)


@router.message(DeleteResumeState.accept, F.text == "Да, удалить")
async def accept_delete_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await delete_document(message, state, repo)
