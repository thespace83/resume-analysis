from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from models.resume import FilterTypes
from repositories.resumes_repo import ResumesRepository
from states import FiltersState
from utils.messages.find import activate_find_document
from utils.messages.select_filter import activate_filter

FILTER_FIELD: dict[FilterTypes, str] = {
    FilterTypes.NAME: "name",
    FilterTypes.PROFESSION: "profession",
    FilterTypes.INFO: "info",
    FilterTypes.GENDER: "gender",
    FilterTypes.OWN_CAR: "own_car",
    FilterTypes.AGE: "age",
    FilterTypes.EDUCATION: "education",
    FilterTypes.EXPERIENCE: "experience",
    FilterTypes.REGION: "region",
    FilterTypes.TYPE_OF_EMPLOYMENT: "type_of_employment",
}

GENDERS = {"Мужчина", "Женщина"}
OWN_CAR_VARIANTS = {"Да", "Нет"}


async def apply_filter(
        message: Message,
        state: FSMContext,
        repo: ResumesRepository,
        target: FilterTypes,
) -> None:
    text = message.text
    if text is None:
        return

    if target == FilterTypes.GENDER and text not in GENDERS:
        await message.answer("Выберите \"Мужчина\" или \"Женщина\".")
        return

    if target == FilterTypes.OWN_CAR and text not in OWN_CAR_VARIANTS:
        await message.answer("Выберите \"Да\" или \"Нет\".")
        return

    if target == FilterTypes.AGE and (text[0] not in {"=", "<", ">"} or not text[1:].isdigit()):
        await activate_filter(message, state, FiltersState.select_age)
        return

    if target == FilterTypes.EXPERIENCE and (text[0] not in {"=", "<", ">"} or not text[1:].isdigit()):
        await activate_filter(message, state, FiltersState.select_experience)
        return

    field = FILTER_FIELD[target]
    await state.update_data(**{field: text})
    await state.set_state(FiltersState.select_filter)
    await activate_find_document(message, state, repo)


async def reset_filters(
        message: Message,
        state: FSMContext,
        repo: ResumesRepository,
        filter_type: FilterTypes
) -> None:
    text = message.text
    if text is None:
        return

    field = FILTER_FIELD[filter_type]
    await state.update_data(**{field: None})
    await activate_find_document(message, state, repo)
