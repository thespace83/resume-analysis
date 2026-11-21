from typing import Callable
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.default import apply_filters_keyboard, select_gender_keyboard
from models.resume import FilterTypes
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
    )
}


async def activate_filter(
        message: Message,
        state: FSMContext,
        target_state: FiltersState,
) -> None:
    print(target_state)
    answer = ANSWER[target_state]
    await state.set_state(target_state)
    await message.answer(
        answer[0],
        reply_markup=answer[1]()
    )
