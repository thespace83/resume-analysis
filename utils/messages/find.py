import os

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from keyboards.default import get_find_files_keyboard
from keyboards.default.find_kb import get_file_watching_keyboard
from keyboards.default.filers_kb import get_select_filter_keyboard
from models.resume import Resume
from repositories.resumes_repo import ResumesRepository
from states import FiltersState, FindResumeState


async def activate_find_document(
        message: Message,
        state: FSMContext,
        repo: ResumesRepository
) -> None:
    await state.set_state(FindResumeState.watching)

    await message.answer(
        await create_filters_message(state)
    )
    await message.answer(
        await create_resumes_message(state, repo),
        reply_markup=get_find_files_keyboard()
    )


async def activate_filters(
        message: Message,
        state: FSMContext,
) -> None:
    await state.set_state(FiltersState.select_filter)
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


async def create_resumes_message(
        state: FSMContext,
        repo: ResumesRepository
) -> str:
    name = await state.get_value("name")
    profession = await state.get_value("profession")
    info = await state.get_value("info")
    gender = await state.get_value("gender")
    own_car = await state.get_value("own_car")

    msg: str = f"Найдено {await repo.get_count_of_resumes(
        name=name,
        profession=profession,
        info=info,
        gender=gender,
        own_car=own_car
    )} файлов\n\n"

    for table_id, resume in (await repo.get_resumes(
            10, 0,
            name=name,
            profession=profession,
            info=info,
            gender=gender,
            own_car=own_car,
    )).items():
        msg += f"#{table_id}: {resume.name if resume.name else 'Без имени'}\n"

    msg += "\n<code>#номер</code> — исследовать файл"
    return msg


async def create_filters_message(
        state: FSMContext,
) -> str:
    params = {
        "name": "Имя",
        "profession": "Профессия",
        "info": "Доп. информация",
        "gender": "Гендер",
        "own_car": "Свой автомобиль",
    }

    filters = ""
    exists = False
    for param, name in params.items():
        value = await state.get_value(param)
        if value is not None:
            exists = True
            filters += f" {name}: {value}\n"

    if exists:
        return "Активированные фильтры:\n" + filters
    else:
        return "Фильтров не добавлено"
