from __future__ import annotations

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_select_filter_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Имя"),
        KeyboardButton(text="Возраст"),
        KeyboardButton(text="Гендер"),
    )
    builder.row(
        KeyboardButton(text="Образование"),
        KeyboardButton(text="Профессия"),
        KeyboardButton(text="Опыт работы"),
    )
    builder.row(
        KeyboardButton(text="Регион"),
        KeyboardButton(text="Тип занятости"),
        KeyboardButton(text="Гражданство"),
    )
    builder.row(
        KeyboardButton(text="Доп. информация"),
        KeyboardButton(text="Водительские права"),
        KeyboardButton(text="Свой автомобиль"),
    )
    builder.row(KeyboardButton(text="Отмена"))
    return builder.as_markup(resize_keyboard=True)
