from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.default import apply_filters_keyboard
from states import FiltersState


async def activate_name_filters(
        message: Message,
        state: FSMContext,
) -> None:
    await state.set_state(FiltersState.select_name)
    await message.answer(
        "Введите имя или часть имени кандидата",
        reply_markup=apply_filters_keyboard()
    )


async def activate_profession_filters(
        message: Message,
        state: FSMContext,
) -> None:
    await state.set_state(FiltersState.select_profession)
    await message.answer(
        "Введите название или часть названия профессии кандидата",
        reply_markup=apply_filters_keyboard()
    )


async def activate_info_filters(
        message: Message,
        state: FSMContext,
) -> None:
    await state.set_state(FiltersState.select_info)
    await message.answer(
        "Введите ключевое слово/предложение из информации о кандидате",
        reply_markup=apply_filters_keyboard()
    )
