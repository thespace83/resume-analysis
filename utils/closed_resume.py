import logging

from aiogram import Bot
from aiogram.types import Document

from repositories.resumes_repo import ResumesRepository
from utils.file_service import extract_context, get_document_url
from utils.publish_resume import download_document


async def find_similar_document(bot: Bot, repo: ResumesRepository, document: Document) -> list[int]:
    await download_document(bot, document)

    context = extract_context(get_document_url(document))

    return await repo.find_similar_resumes(context)
