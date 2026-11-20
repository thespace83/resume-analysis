from __future__ import annotations

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from repositories.resumes_repo import ResumesRepository
from states import MenuState
from utils.messages.find import activate_find_document

router = Router(name="users:find")


@router.message(MenuState.menu, F.text == "Поиск")
async def find_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await activate_find_document(message, state, repo)
