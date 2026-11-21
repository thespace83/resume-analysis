from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.default.filers_kb import get_select_filter_keyboard
from repositories.resumes_repo import ResumesRepository
from states import FiltersState


async def activate_name_filters(
        message: Message,
        state: FSMContext,
        repo: ResumesRepository
) -> None:
    await state.set_state(FiltersState.select_filter)
    await message.answer(
        "Выберите значение",
        reply_markup=get_select_filter_keyboard()
    )
