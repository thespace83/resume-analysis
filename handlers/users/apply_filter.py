from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from models.resume import FilterTypes
from repositories.resumes_repo import ResumesRepository
from states import FiltersState
from utils.messages.apply_filter import apply_filter, reset_filters
from utils.messages.find import activate_filters

router = Router(name="users:apply_filter")

FILTER_STATES = (
    FiltersState.select_name,
    FiltersState.select_education,
    FiltersState.select_age,
    FiltersState.select_profession,
    FiltersState.select_info,
    FiltersState.select_gender,
    FiltersState.select_own_car,
    FiltersState.select_experience,
    FiltersState.select_region,
    FiltersState.select_type_of_employment,
    FiltersState.select_citizenship,
)

STATE_TO_FILTER: dict[str, FilterTypes] = {
    FiltersState.select_name.state: FilterTypes.NAME,
    FiltersState.select_education.state: FilterTypes.EDUCATION,
    FiltersState.select_age.state: FilterTypes.AGE,
    FiltersState.select_profession.state: FilterTypes.PROFESSION,
    FiltersState.select_info.state: FilterTypes.INFO,
    FiltersState.select_gender.state: FilterTypes.GENDER,
    FiltersState.select_own_car.state: FilterTypes.OWN_CAR,
    FiltersState.select_experience.state: FilterTypes.EXPERIENCE,
    FiltersState.select_region.state: FilterTypes.REGION,
    FiltersState.select_type_of_employment.state: FilterTypes.TYPE_OF_EMPLOYMENT,
    FiltersState.select_citizenship.state: FilterTypes.CITIZENSHIP,
}


async def _current_filter_type(state: FSMContext) -> FilterTypes | None:
    return STATE_TO_FILTER.get(await state.get_state())


@router.message(StateFilter(*FILTER_STATES), F.text == "Отмена")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    await activate_filters(message, state)


@router.message(StateFilter(*FILTER_STATES), F.text == "Сбросить")
async def reset_handler(
        message: Message, state: FSMContext, repo: ResumesRepository
) -> None:
    filter_type = await _current_filter_type(state)
    if filter_type is None:
        return
    await reset_filters(message, state, repo, filter_type)


@router.message(StateFilter(*FILTER_STATES), F.text)
async def apply_handler(
        message: Message, state: FSMContext, repo: ResumesRepository
) -> None:
    filter_type = await _current_filter_type(state)
    if filter_type is None:
        return
    await apply_filter(message, state, repo, filter_type)
