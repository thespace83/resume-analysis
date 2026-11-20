from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.default import get_cancel_keyboard
from repositories.resumes_repo import ResumesRepository
from states.find_resume import FindResumeState


async def activate_find_document(
        message: Message,
        state: FSMContext,
        repo: ResumesRepository
) -> None:
    async def create_message() -> str:
        msg: str = f"Доступно {await repo.get_count_of_resumes()} файлов\n\n"
        for table_id, resume in (await repo.get_resumes(5, 0)).items():
            msg += f"{table_id}> {resume.name if resume.name else 'Без имени'}\n"
        msg += "\nВыставленные фильтры:"
        return msg

    await state.set_state(FindResumeState.watching)
    await message.answer(
        await create_message(),
        reply_markup=get_cancel_keyboard()
    )
