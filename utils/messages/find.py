import os

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from keyboards.default import get_cancel_and_update_keyboard
from keyboards.default.filers_kb import get_file_watching_keyboard
from models.resume import Resume
from repositories.resumes_repo import ResumesRepository
from states.find_resume import FindResumeState


async def create_message(repo: ResumesRepository) -> str:
    msg: str = f"Доступно {await repo.get_count_of_resumes()} файлов\n\n"

    for table_id, resume in (await repo.get_resumes(10, 0)).items():
        msg += f"#{table_id}: {resume.name if resume.name else 'Без имени'}\n"

    msg += "\n<code>#номер</code> — исследовать файл"
    return msg


async def get_info(number: int, repo: ResumesRepository) -> str | None:
    resume: Resume | None = await repo.get_resume(number)
    if resume is None:
        return None

    msg = f"Имя: {resume.name or ''}\n"
    msg += f"Возраст: {resume.age if resume.age is not None else ''}\n"
    msg += f"Гендер: {resume.gender or ''}\n"
    msg += f"Образование: {resume.education or ''}\n"
    msg += f"Регион: {resume.region or ''}\n"
    msg += f"Профессия: {resume.profession or ''}\n"
    msg += f"Опыт: {resume.experience if resume.experience is not None else ''}\n"
    msg += f"Тип занятости: {resume.type_of_employment or ''}\n"
    msg += f"Доп. информация: {resume.info or ''}\n"
    msg += f"Водительские права: {resume.driving_license_category or ''}\n"
    msg += f"Свой автомобиль: {resume.own_car or ''}\n"
    msg += f"Гражданство: {resume.citizenship or ''}\n"
    return msg


async def activate_find_document(
        message: Message,
        state: FSMContext,
        repo: ResumesRepository
) -> None:
    await state.set_state(FindResumeState.watching)
    await message.answer(
        await create_message(repo),
        reply_markup=get_cancel_and_update_keyboard()
    )


async def examine_file(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    if message.text is None:
        await activate_find_document(message, state, repo)
        return

    if message.text[0] == "#" and message.text[1:].isdigit():
        number = int(message.text[1:])
        resume: Resume | None = await repo.get_resume(number)
        if resume is None:
            await activate_find_document(message, state, repo)
            return

        document_url: str = resume.document_url
        document = FSInputFile(os.path.join(os.getcwd(), "documents", document_url),
                               filename="Резюме.pdf")

        await state.set_state(FindResumeState.watching_target)
        await state.update_data(target=number)
        await message.answer_document(
            caption=await get_info(number, repo),
            document=document,
            reply_markup=get_file_watching_keyboard()
        )
