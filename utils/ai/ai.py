import logging
import traceback

import openai

from data.config import settings
from models.resume import Resume
from utils.ai.external_ai_service import ExternalAIService

client = openai.OpenAI(
    api_key=settings.YANDEX_CLOUD_API_KEY,
    base_url="https://ai.api.cloud.yandex.net/v1",
    project=settings.YANDEX_CLOUD_FOLDER
)

external_ai_service = ExternalAIService(
    client=client,
    yandex_cloud_folder=settings.YANDEX_CLOUD_FOLDER,
    yandex_cloud_model=settings.YANDEX_CLOUD_MODEL,
)


def get_resume(document_url: str, context: str) -> Resume:
    try:
        data: dict = external_ai_service.request(context)
        return Resume(
            document_url=document_url,
            name=str(data['name']),
            age=None if int(data['age']) == -1 else int(data['age']),
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
    except Exception as e:
        logging.error(e)
        traceback.print_exc()
