import logging
import traceback

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, Document

from exeptions.not_open_resume import NotOpenResume
from keyboards.default import get_cancel_keyboard
from repositories.resumes_repo import ResumesRepository
from states import LoadResumeState, MenuState
from utils.messages.menu import activate_main_menu
from utils.publish_resume import publish_document


async def activate_load_open_document(
        message: Message,
        state: FSMContext
) -> None:
    await state.set_state(LoadResumeState.waiting_for_open_document)
    await message.answer(
        f"Загрузите документы\n\nДоступные форматы: pdf, docx",
        reply_markup=get_cancel_keyboard()
    )


async def activate_load_closed_document(
        message: Message,
        state: FSMContext
) -> None:
    await state.set_state(LoadResumeState.waiting_for_close_document)
    await message.answer(
        f"Загрузите документ\n\nДоступные форматы: pdf, docx",
        reply_markup=get_cancel_keyboard(),
    )


async def start_load_documents(
        message: Message,
        repo: ResumesRepository,
        state: FSMContext,
) -> None:
    await state.set_state(MenuState.menu)
    await message.answer(
        f"Вы можете продолжать работу\n\n"
        "Документы обрабатывается и через некоторое время будут доступны"
    )
    await activate_main_menu(message, state, repo)


async def load_document(
        bot: Bot,
        message: Message,
        repo: ResumesRepository,
) -> None:
    if message.document is None:
        logging.error("The document has not been delivered.")
        return

    document = message.document
    logging.debug(f"The user uploaded a new document: {document}")

    document_name = document.file_name

    if not is_document_correct(document):
        await message.answer(
            f"Не удалось загрузить документ {document_name}"
            "Бот поддерживает форматы .pdf и .docx"
            "Максимальный размер файла 20МБ"
        )

    try:
        await publish_document(bot, repo, document)
    except NotOpenResume:
        await message.reply(
            text=f"Документ {document_name} не открытое резюме"
        )
    except Exception as err:
        await message.reply(
            text=f"Документ {document_name} не загрузился, попробуйте ещё раз"
        )
        logging.error(err)
        traceback.print_exc()


def is_document_correct(document: Document) -> bool:
    if document.file_name is None:
        return False

    document_name: str = document.file_name
    document_size = document.file_size
    return is_format_available(document_name) and is_size_correct(document_size)


def is_format_available(name: str | None) -> bool:
    return (name is not None) and (name.split(".")[-1:][0] == "pdf" or name.split(".")[-1:][0] == "docx")


def is_size_correct(size: int | None) -> bool:
    return (size is not None) and (size < 20 * 1024 * 1024)
