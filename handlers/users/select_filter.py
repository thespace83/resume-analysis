from __future__ import annotations

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from repositories.resumes_repo import ResumesRepository
from states import FiltersState
from utils.messages.select_filter import activate_filter
from utils.messages.find_documents import activate_find_document, activate_filters

router = Router(name="users:select_filter")

TYPES: dict[str, FiltersState] = {
    "Имя": FiltersState.select_name,
    "Возраст": FiltersState.select_age,
    "Гендер": FiltersState.select_gender,
    "Образование": FiltersState.select_education,
    "Профессия": FiltersState.select_profession,
    "Доп. информация": FiltersState.select_info,
    "Свой автомобиль": FiltersState.select_own_car,
    "Опыт работы": FiltersState.select_experience,
    "Регион": FiltersState.select_region,
    "Тип занятости": FiltersState.select_type_of_employment,
    "Гражданство": FiltersState.select_citizenship,
    "Водительские права": FiltersState.select_driving_license_category,
    "Знание языков": FiltersState.select_knowledge_of_languages,
}


@router.message(FiltersState.select_filter, F.text == "Отмена")
async def cancel_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await activate_find_document(message, state, repo)


@router.message(FiltersState.select_filter)
async def filter_handler(message: Message, state: FSMContext) -> None:
    text = message.text
    if text is None:
        await activate_filters(message, state)
        return
    if text not in TYPES:
        await activate_filters(message, state)
        return
    await activate_filter(message, state, TYPES[text])
