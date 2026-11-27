import asyncio
import os

import docx
from aiogram import Bot
from aiogram.types import Document
from pypdf import PdfReader

from models.resume import Resume
from repositories.resumes_repo import ResumesRepository
from utils.ai.ai import get_resume


def extract_text_pdf(path: str) -> str:
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
        text += "\n"
    return text


def extract_text_docx(path: str) -> str:
    doc = docx.Document(path)
    return '\n'.join([para.text for para in doc.paragraphs])


async def publish_document(bot: Bot, repo: ResumesRepository, document: Document):
    file_type = str(document.file_name).split(".")[-1]
    await bot.download(document, destination=os.path.join(os.getcwd(), "documents", f"{document.file_id}.{file_type}"))

    def _process() -> Resume:
        document_url = f"{document.file_id}.{file_type}"
        path = os.path.join("documents", document_url)
        context: str = extract_text_pdf(path) if file_type == "pdf" else extract_text_docx(path)
        return get_resume(document_url, context)

    resume = await asyncio.to_thread(_process)
    await repo.create(resume)
