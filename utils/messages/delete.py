from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from repositories.resumes_repo import ResumesRepository
from states import MenuState, DeleteResumeState
from keyboards.default import get_delete_keyboard
from utils.messages.find import activate_find_document


async def activate_delete_menu(
        message: Message,
        state: FSMContext,
        repo: ResumesRepository,
) -> None:
    await state.set_state(DeleteResumeState.accept)
    await message.answer(
        text="Вы уверены, что хотите удалить резюме?",
        reply_markup=get_delete_keyboard())


async def delete_document(
        message: Message,
        state: FSMContext,
        repo: ResumesRepository,
) -> None:
    resume_id = await state.get_value("target")
    await repo.delete(resume_id)
    await message.answer(text=f"Резюме #{resume_id} удалено")
    await activate_find_document(message, state, repo)
