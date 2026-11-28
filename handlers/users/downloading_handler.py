from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from repositories.resumes_repo import ResumesRepository
from states import FindResumeState


router = Router(name="users:downloading")

@router.message(FindResumeState.watching, F.text == "Скачать")
async def update_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await activate_find_document(message, state, repo)

