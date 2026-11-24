import asyncio
import logging
import os

from aiogram import Bot
from aiogram.types import Document

from pypdf import PdfReader
import docx

from models.resume import Resume
from repositories.resumes_repo import ResumesRepository
from utils.ai import generate_resume_data


def extract_text_pdf(path: str) -> str:
    """Extract text from PDF file

    parameters:
    pdf_path: Path to PDF file
    """
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
        text += "\n"
    return text


def extract_text_docx(path: str) -> str:
    """Extract text from DOCX file"""
    doc = docx.Document(path)
    return '\n'.join([para.text for para in doc.paragraphs])


async def publish_document(bot: Bot, repo: ResumesRepository, document: Document):
    """
    Publish resume document

    parameters:
    document: Resume document file_id
    """
    file_type = document.file_name.split(".")[-1]
    await bot.download(document, destination=os.path.join(os.getcwd(), "documents", f"{document.file_id}.{file_type}"))

    logging.info(f"File T: {file_type}")

    def _process():
        path = os.path.join("documents", f"{document.file_id}.{file_type}")
        context: str = extract_text_pdf(path) if file_type == "pdf" else extract_text_docx(path)
        data = generate_resume_data(context)
        return Resume(
            url=f"{document.file_id}.{file_type}",
            name=str(data['name']),
            age=None if int(data['age']) == -1 else int(data['age']),
            gender=str(data['gender']),
            education=str(data['education']),
            region=str(data['region']),
            profession=str(data['profession']),
            work_experience=int(data['experience']),
            type_of_employment=str(data['type-of-employment']),
            info=str(data['info']),
            knowledge_of_languages=list[dict[str, str]](data['knowledge-of-languages']),
            driving_license_category=str(data['driving-license-category']),
            own_car=str(data['own-car']),
            citizenship=str(data['citizenship']),
            context=context
        )

    resume = await asyncio.to_thread(_process)
    await repo.create(resume)
