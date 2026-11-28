import asyncio
import os

from aiogram import Bot
from aiogram.types import Document

from exeptions.not_open_resume import NotOpenResume
from models.resume import Resume
from repositories.resumes_repo import ResumesRepository
from utils.ai.ai import get_resume
from utils.file_service import extract_context, download_document, get_document_url


async def publish_document(bot: Bot, repo: ResumesRepository, document: Document):
    await download_document(bot, document)

    def _process() -> Resume:
        document_url: str = get_document_url(document)
        context: str = extract_context(document_url)
        return get_resume(document_url, context)

    resume = await asyncio.to_thread(_process)
    if resume.name == "":
        raise NotOpenResume
    await repo.create(resume)
