import json
import logging
import traceback
from typing import Any

from openai import OpenAI
from openai.types.responses import ParsedResponse, ParsedResponseOutputMessage, ParsedResponseOutputText

from utils.ai.resume_format import resume_format


class ExternalAIService:
    def __init__(self, client: OpenAI, yandex_cloud_folder: str, yandex_cloud_model: str):
        self.client: OpenAI = client
        self.yandex_cloud_folder: str = yandex_cloud_folder
        self.yandex_cloud_model: str = yandex_cloud_model

    def request(self, context: str) -> dict:
        try:
            response: ParsedResponse[Any] = self.client.responses.parse(
                model=f"gpt://{self.yandex_cloud_folder}/{self.yandex_cloud_model}",
                temperature=0,
                instructions="""
Выведи машинно-читаемые данные без форматирования о кандидате в формате JSON. 
Ключ "name": ФИО кандидата, если не найдено, пустая строка. 
Ключ "age": возраст кандидата, если не найдено, -1. 
Ключ "gender": пол кандидата, если не найдено, пустая строка. 
Ключ "education": образование кандидата, если не найдено, пустая строка. 
Ключ "region": регион РФ в котором кандидат ищет работу, если не найдено пустая строка. 
Ключ "profession": профессия кандидата, если не найдено, пустая строка.
Ключ "experience": количество лет работы кандидата, если не найдено, -1. 
Ключ "type-of-employment": тип работы кандидата, если не найдено, пустая строка. 
Ключ "info": вырезка из текста про личные качества кандидата, если не найдено, пустая строка. 
Ключ "knowledge-of-languages": список из словарей, где ключ название языка строчными буквами, а значение уровень владения языком, если язык родной, то указать \"родной\", если не найдено, пустой список. 
Ключ "driving-license-category": категория прав кандидата, если не найдено, пустая строка. 
Ключ "own-car": "да" если у кандидата есть своя машина, "нет" если у кандидата нет свей машины, если не найдено, пустая строка. 
Ключ "citizenship": название страны, гражданином которой является кандидат, если не найдено, пустая строка.
""",
                input=context,
                max_output_tokens=65536,
                store=False,
                truncation="disabled",
                text=resume_format,
            )
            output: ParsedResponseOutputMessage = response.output[0]
            content: ParsedResponseOutputText = output.content[0]
            return json.loads(content.text)
        except Exception as e:
            logging.error(e.__traceback__)
            traceback.print_exc()

        raise
