from __future__ import annotations

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_select_filter_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Отмена"),
        KeyboardButton(text="Имя"),
        KeyboardButton(text="Возраст"),
        KeyboardButton(text="Гендер"),
        KeyboardButton(text="Образование"),
        KeyboardButton(text="Регион"),
        KeyboardButton(text="Профессия"),
        KeyboardButton(text="Опыт работы"),
        KeyboardButton(text="Тип занятости"),
        KeyboardButton(text="Доп. информация"),
        KeyboardButton(text="Водительские права"),
        KeyboardButton(text="Свой автомобиль"),
        KeyboardButton(text="Гражданство"),
    )
    return builder.as_markup(resize_keyboard=True)
