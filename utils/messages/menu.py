from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.default import get_menu_keyboard
from repositories.resumes_repo import ResumesRepository
from states import MenuState


async def activate_main_menu(
        message: Message,
        state: FSMContext,
        repo: ResumesRepository,
) -> None:
    await state.set_state(MenuState.menu)
    await message.answer(
        "Аналитика Резюме\n\n"
        'Чтобы загрузить резюме используйте "Загрузка"\n'
        'Чтобы найти резюме используйте "Поиск"\n',
        reply_markup=get_menu_keyboard(),
    )
    await message.answer(f"Доступных документов: {await repo.get_count_of_resumes()}")
