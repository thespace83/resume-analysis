from __future__ import annotations

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from repositories.resumes_repo import ResumesRepository
from states import FiltersState
from utils.messages.select_filter import activate_name_filters
from utils.messages.find import activate_find_document

router = Router(name="users:select_filter")


@router.message(FiltersState.select_filter, F.text == "Имя")
async def name_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await activate_name_filters(message, state, repo)


@router.message(FiltersState.select_filter, F.text == "Возраст")
async def name_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await activate_name_filters(message, state, repo)


@router.message(FiltersState.select_filter, F.text == "Гендер")
async def name_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await activate_name_filters(message, state, repo)


@router.message(FiltersState.select_filter, F.text == "Образование")
async def name_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await activate_name_filters(message, state, repo)


@router.message(FiltersState.select_filter, F.text == "Профессия")
async def name_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await activate_name_filters(message, state, repo)


@router.message(FiltersState.select_filter, F.text == "Опыт работы")
async def name_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await activate_name_filters(message, state, repo)


@router.message(FiltersState.select_filter, F.text == "Регион")
async def name_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await activate_name_filters(message, state, repo)


@router.message(FiltersState.select_filter, F.text == "Тип занятости")
async def name_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await activate_name_filters(message, state, repo)


@router.message(FiltersState.select_filter, F.text == "Гражданство")
async def name_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await activate_name_filters(message, state, repo)


@router.message(FiltersState.select_filter, F.text == "Доп. информация")
async def name_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await activate_name_filters(message, state, repo)


@router.message(FiltersState.select_filter, F.text == "Водительские права")
async def name_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await activate_name_filters(message, state, repo)


@router.message(FiltersState.select_filter, F.text == "Свой автомобиль")
async def name_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await activate_name_filters(message, state, repo)


@router.message(FiltersState.select_filter, F.text == "Отмена")
async def name_handler(message: Message, state: FSMContext, repo: ResumesRepository) -> None:
    await activate_find_document(message, state, repo)
