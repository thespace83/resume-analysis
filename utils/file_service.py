import os

import docx
from aiogram import Bot
from aiogram.types import Document
from pypdf import PdfReader


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


def extract_context(document_url: str) -> str:
    path = os.path.join("documents", document_url)
    file_type = str(document_url).split(".")[-1]
    return extract_text_pdf(path) if file_type == "pdf" else extract_text_docx(path)


async def download_document(bot: Bot, document: Document):
    file_type = str(document.file_name).split(".")[-1]
    await bot.download(document, destination=os.path.join(os.getcwd(), "documents", f"{document.file_id}.{file_type}"))


def get_document_url(document: Document) -> str:
    file_type = str(document.file_name).split(".")[-1]
    return f"{document.file_id}.{file_type}"
