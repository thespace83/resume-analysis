from __future__ import annotations

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_find_files_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Отмена"),
        KeyboardButton(text="Фильтры"),
        KeyboardButton(text="Обновить"),
    )
    return builder.as_markup(resize_keyboard=True)
