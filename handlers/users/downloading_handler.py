from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from repositories.resumes_repo import ResumesRepository
from states import FindResumeState
from utils.messages.downloading_documents import downloading_documents

router = Router(name="users:downloading")

@router.message(FindResumeState.watching, F.text == "Скачать")
async def download_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await downloading_documents(message, state, repo)

