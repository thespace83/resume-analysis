import os

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from keyboards.default import get_find_files_keyboard
from keyboards.default.find_kb import get_file_watching_keyboard
from keyboards.default.filers_kb import get_select_filter_keyboard
from models.resume import Resume
from repositories.resumes_repo import ResumesRepository
from states.find_resume import FindResumeState


async def activate_find_document(
        message: Message,
        state: FSMContext,
        repo: ResumesRepository
) -> None:
    async def create_message() -> str:
        msg: str = f"Доступно {await repo.get_count_of_resumes()} файлов\n\n"

        for table_id, resume in (await repo.get_resumes(10, 0)).items():
            msg += f"#{table_id}: {resume.name if resume.name else 'Без имени'}\n"

        msg += "\n<code>#номер</code> — исследовать файл"
        return msg

    await state.set_state(FindResumeState.watching)
    await message.answer(
        await create_message(),
        reply_markup=get_find_files_keyboard()
    )


async def activate_filters(
        message: Message,
        state: FSMContext,
        repo: ResumesRepository
) -> None:
    await state.set_state(FindResumeState.select_filter)
    await message.answer(
        "Выберите желаемый фильтр",
        reply_markup=get_select_filter_keyboard()
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

        async def get_info() -> str | None:
            r: Resume | None = await repo.get_resume(number)
            if r is None:
                return None

            msg = f"Имя: {r.name or ''}\n"
            msg += f"Возраст: {r.age if r.age is not None else ''}\n"
            msg += f"Гендер: {r.gender or ''}\n"
            msg += f"Образование: {r.education or ''}\n"
            msg += f"Регион: {r.region or ''}\n"
            msg += f"Профессия: {r.profession or ''}\n"
            msg += f"Опыт: {r.experience if r.experience is not None else ''}\n"
            msg += f"Тип занятости: {r.type_of_employment or ''}\n"
            msg += f"Доп. информация: {r.info or ''}\n"
            msg += f"Водительские права: {r.driving_license_category or ''}\n"
            msg += f"Свой автомобиль: {r.own_car or ''}\n"
            msg += f"Гражданство: {r.citizenship or ''}\n"
            return msg

        await message.answer_document(
            caption=await get_info(),
            document=document,
            reply_markup=get_file_watching_keyboard()
        )
