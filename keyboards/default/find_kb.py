from __future__ import annotations

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_find_files_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Фильтры"),
        KeyboardButton(text="Обновить"),
        KeyboardButton(text="Скачать"),
    )
    builder.row(
        KeyboardButton(text="Отмена"),
    )
    return builder.as_markup(resize_keyboard=True)


def get_file_watching_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Назад"),
        KeyboardButton(text="Удалить"),
    )
    return builder.as_markup(resize_keyboard=True)
