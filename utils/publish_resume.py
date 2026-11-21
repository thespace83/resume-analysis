import asyncio
import os

from aiogram import Bot
from aiogram.types import Downloadable
from pypdf import PdfReader

from models.resume import Resume
from repositories.resumes_repo import ResumesRepository
from utils.ai import generate_resume_data


def extract_text_pdf(pdf_path: str) -> str:
    """Extract text from PDF file

    parameters:
    pdf_path: Path to PDF file
    """
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
        text += "\n"
    return text


async def publish_document(bot: Bot, repo: ResumesRepository, document: Downloadable):
    """
    Publish resume document

    parameters:
    document: Resume document file_id
    """
    await bot.download(document, destination=os.path.join(os.getcwd(), "documents", f"{document.file_id}.pdf"))

    def _process():
        path = os.path.join("documents", f"{document.file_id}.pdf")
        context: str = extract_text_pdf(path)
        data = generate_resume_data(context)
        return Resume(
            document_url=f"{document.file_id}.pdf",
            name=str(data['name']),
            age=int(data['age']),
            gender=str(data['gender']),
            education=str(data['education']),
            region=str(data['region']),
            profession=str(data['profession']),
            experience=int(data['experience']),
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
