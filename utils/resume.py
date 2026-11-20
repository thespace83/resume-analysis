import os
from typing import Optional

from aiogram import Bot
from aiogram.types import Downloadable
from pypdf import PdfReader

from utils.ai import generate_resume


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


async def publish_document(bot: Bot, document: Downloadable):
    """
    Publish resume document

    parameters:
    document: Resume document file_id
    """
    await bot.download(document, destination=os.path.join(os.getcwd(), "documents", f"{document.file_id}.pdf"))
    context: str = extract_text_pdf(
        os.path.join("documents", f"{document.file_id}.pdf")
    )
    resume: Resume = create_resume(
        generate_resume(context)
    )


def create_resume(data: dict) -> Resume:
    resume = Resume('')
    resume.name = str(data['name'])
    resume.age = int(data['age'])
    resume.gender = str(data['gender'])
    resume.education = str(data['education'])
    resume.region = str(data['region'])
    resume.profession = str(data['profession'])
    resume.experience = int(data['experience'])
    resume.type_of_employment = str(data['type-of-employment'])
    resume.info = str(data['info'])
    resume.knowledge_of_languages = list[dict[str, str]](data['knowledge-of-languages'])
    resume.driving_license_category = str(data['driving-license-category'])
    resume.own_car = str(data['own-car'])
    resume.citizenship = str(data['citizenship'])
    return resume


class Resume:
    """Resume class
    Attributes:
        document_url: Resume document_url
        name: Resume name
        age: Resume age
        gender: Resume gender
        education: Resume education
        region: Resume region
        profession: Resume profession
        experience: Resume experience
        type_of_employment: Resume type_of_employment
        info: Resume information
        knowledge_of_languages: Resume knowledge_of_languages
        driving_license_category: Resume driving_license_category
        own_car: Resume own_car
        citizenship: Resume citizenship
        """

    def __init__(self, document_url: str):
        self.document_url = document_url
        self.name: Optional[str] = None
        self.age: Optional[int] = None
        self.gender: Optional[str] = None
        self.education: Optional[str] = None
        self.region: Optional[str] = None
        self.profession: Optional[str] = None
        self.experience: Optional[int] = None
        self.type_of_employment: Optional[str] = None
        self.info: Optional[str] = None
        self.knowledge_of_languages: Optional[list[dict[str, str]]] = None
        self.driving_license_category: Optional[str] = None
        self.own_car: Optional[str] = None
        self.citizenship: Optional[str] = None

    def __str__(self):
        return str(self.__dict__)
