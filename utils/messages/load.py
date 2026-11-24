import logging

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.default import get_menu_keyboard, get_cancel_keyboard
from repositories.resumes_repo import ResumesRepository
from states import MenuState, LoadResumeState
from utils.messages.menu import activate_main_menu
from utils.publish_resume import publish_document


async def activate_load_document(
        message: Message,
        state: FSMContext
) -> None:
    await state.set_state(LoadResumeState.waiting_for_document)
    await message.answer(
        f"Загрузите Ваш документ\n\nДоступные форматы: pdf, docx",
        reply_markup=get_cancel_keyboard()
    )


async def load_document(
        bot: Bot,
        message: Message,
        state: FSMContext,
        repo: ResumesRepository,
) -> None:
    if message.document is None:
        logging.error("The document has not been delivered.")
        return
    document = message.document

    if not is_available_format(document.file_name):
        await message.answer(f"Формат \".{document.file_name.split(".")[-1:][0]}\" не поддерживается")
        return
    if not has_correct_size(document.file_size):
        await message.answer(f"Файл весит больше лимита в 20 MB")
        return

    await state.set_state(MenuState.menu)
    await message.answer(
        f"Вы можете продолжать работу\n\nДокумент обрабатывается и через некоторое время будет доступен",
        reply_markup=get_menu_keyboard())
    await activate_main_menu(message, state, repo)

    try:
        await publish_document(bot, repo, document)
    except TimeoutError:
        await message.reply(
            text="Документ не загрузился, попробуйте ещё раз"
        )
    except Exception as err:
        logging.error(err)


def is_available_format(file_name: str | None) -> bool:
    return (file_name is not None) and (file_name.split(".")[-1:][0] == "pdf" or file_name.split(".")[-1:][0] == "docx")


def has_correct_size(file_size: int | None) -> bool:
    return (file_size is not None) and (file_size < 20 * 1024 * 1024)
