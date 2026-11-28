import logging
import os

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from keyboards.default import get_delete_keyboard
from models.resume import Resume
from repositories.resumes_repo import ResumesRepository
from states.downloading import DownloadingState
from utils.file_service import get_document
from utils.messages.find_documents import activate_find_document


async def downloading_documents(
        message: Message,
        state: FSMContext,
        repo: ResumesRepository,
) -> None:
    await state.set_state(DownloadingState.downloading)
    logging.info(f"{await state.get_value("targets")}")
    if await state.get_value("targets") is not None:
        for target in await state.get_value("targets"):
            resume: Resume | None = await repo.get_resume(target)
            if resume is None:
                raise

            await message.answer_document(
                caption=resume.name if resume.name else "",
                document=get_document(resume.document_url)
            )
    else:
        await activate_find_document(message, state, repo)
