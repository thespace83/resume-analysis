from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from models.resume import FilterTypes
from states import FiltersState
from utils.messages.find import activate_filters


async def apply_name_filters(
        message: Message,
        state: FSMContext,
) -> None:
    if message.text is None:
        return
    await message.answer(f"Не добавлен фильтр \"{await state.get_value("name")}\" для имени кандидата")
    await state.update_data(name=message.text.lower())
    await state.set_state(FiltersState.select_filter)
    await message.answer(f"Добавлен фильтр \"{await state.get_value("name")}\" для имени кандидата")
    await activate_filters(message, state)


async def reset_filters(
        state: FSMContext,
        filter_type: FilterTypes
) -> None:
    if filter_type == FilterTypes.NAME:
        await state.update_data(name=None)
