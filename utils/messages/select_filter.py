from typing import Callable

from aiogram import html
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.default import apply_filters_keyboard, select_gender_keyboard, select_own_car_keyboard, \
    select_education_keyboard, select_type_of_employment_keyboard, select_driving_license_category_keyboard
from states import FiltersState

ANSWER: dict[FiltersState, tuple[str, Callable]] = {
    FiltersState.select_name: (
        "Введите имя или часть имени кандидата",
        apply_filters_keyboard,
    ),
    FiltersState.select_profession: (
        "Введите название или часть названия профессии кандидата",
        apply_filters_keyboard,

    ),
    FiltersState.select_info: (
        "Введите ключевое слово/предложение из информации о кандидате",
        apply_filters_keyboard,

    ),
    FiltersState.select_gender: (
        "Выберите гендер кандидата",
        select_gender_keyboard,
    ),
    FiltersState.select_own_car: (
        "Укажите, есть ли у кандидата автомобиль",
        select_own_car_keyboard
    ),
    FiltersState.select_age: (
        html.quote("Введите возраст кандидата в формате" +
                   "\n=18 для точного указания" +
                   "\n>18 для выбора от 18 и старше" +
                   "\n<18 для выбора от 18 и младше"),
        apply_filters_keyboard,
    ),
    FiltersState.select_education: (
        "Введите уровень образования кандидата",
        select_education_keyboard,
    ),
    FiltersState.select_experience: (
        html.quote("Введите опыт работы кандидата в годах" +
                   "\n=3 для точного указания" +
                   "\n>3 для выбора от 3-х и более лет" +
                   "\n<3 для выбора от 3-х и менее лет"),
        apply_filters_keyboard,
    ),
    FiltersState.select_region: (
        "Введите регион работы кандидата",
        apply_filters_keyboard
    ),
    FiltersState.select_type_of_employment: (
        "Введите тип занятости кандидата",
        select_type_of_employment_keyboard
    ),
    FiltersState.select_citizenship: (
        "Введите гражданство кандидата",
        apply_filters_keyboard
    ),
    FiltersState.select_driving_license_category: (
        "Введите тип водительских прав",
        select_driving_license_category_keyboard
    )
}


async def activate_filter(
        message: Message,
        state: FSMContext,
        target_state: FiltersState,
) -> None:
    answer = ANSWER[target_state]
    await state.set_state(target_state)
    await message.answer(
        answer[0],
        reply_markup=answer[1]()
    )
