import json
import ollama
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

Gender = Literal["мужчина", "женщина", ""]
EmploymentType = Literal["постоянная работа", "подработка", "стажировка", "прочее", ""]
DrivingLicense = Literal["А", "В", "С", "D", "E", ""]
LanguageLevel = Literal["A1", "A2", "B1", "B2", "C1", "C2", "родной"]


class LanguageSkill(BaseModel):
    model_config = ConfigDict(extra="forbid")

    language: str
    level: LanguageLevel | None


class ResumeModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True
    )

    name: str | None
    age: int | None
    gender: Gender | None
    education: str | None
    region: str | None
    profession: str | None
    work_experience: int | None
    type_of_employment: EmploymentType | None = Field(alias="type_of_employment")
    info: str | None
    knowledge_of_languages: list[LanguageSkill] | None = Field(alias="knowledge_of_languages")
    driving_license_category: DrivingLicense | None = Field(alias="driving_license_category")
    own_car: bool | None
    citizenship: str | None


def generate_resume_data(context: str) -> dict:
    prompt = f"""{context}
Извлеки из текста резюме структурированные данные о кандидате.

Правила:
- Не придумывай данные. Если информации нет в тексте — оставь поле пустым
  (пустая строка, -1 для числовых полей, пустой список для языков).
- Регион: если в тексте указан город или неформальное название («Питер», «МСК»),
  выбери именно регин РФ.
- Названия языков и гражданство указывай строчными буквами.
- Опыт работы: укажи целое число полных лет.
- Если в тексте несколько профессий — укажи основную.
- Языки: верни объект, где ключ — название языка строчными буквами,
  значение — уровень владения (например, {{"english": "B1", "russian": "родной"}}).

Пример:
Текст: «Иван Петров, 28 лет, Python-разработчик из Казани. Опыт 5 лет.
Английский — B2. Права категории B, свой автомобиль.»
Ответ: {{"name": "Иван Петров", "age": 28, "region": "Республика Татарстан",
"profession": "Python-разработчик", "experience": 5, ...}}
"""
    schema = ResumeModel.model_json_schema(by_alias=True)
    response = ollama.chat(
        model='qwen3.5:4b',
        messages=[
            {"role": "user",
             "content": prompt},
        ],
        format=schema,
        think=False
    )
    data = json.loads(response['message']['content'])

    return data
