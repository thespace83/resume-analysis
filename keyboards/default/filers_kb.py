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


def apply_filters_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Отмена"),
        KeyboardButton(text="Сбросить"),
    )
    return builder.as_markup(resize_keyboard=True)


def select_gender_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Мужчина"),
        KeyboardButton(text="Женщина"),
    )
    builder.row(
        KeyboardButton(text="Отмена"),
        KeyboardButton(text="Сбросить"),
    )
    return builder.as_markup(resize_keyboard=True)


def select_own_car_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Да"),
        KeyboardButton(text="Нет"),
    )
    builder.row(
        KeyboardButton(text="Отмена"),
        KeyboardButton(text="Сбросить"),
    )
    return builder.as_markup(resize_keyboard=True)


def select_education_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="среднее"),
        KeyboardButton(text="средне специальное"),
        KeyboardButton(text="высшее"),
    )
    builder.row(
        KeyboardButton(text="Отмена"),
        KeyboardButton(text="Сбросить"),
    )
    return builder.as_markup(resize_keyboard=True)


def select_type_of_employment_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="постоянная работа"),
        KeyboardButton(text="подработка"),
        KeyboardButton(text="стажировка"),
    )
    builder.row(
        KeyboardButton(text="Отмена"),
        KeyboardButton(text="Сбросить"),
    )
    return builder.as_markup(resize_keyboard=True)


def select_driving_license_category_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="A"),
        KeyboardButton(text="B"),
        KeyboardButton(text="C"),
        KeyboardButton(text="D"),
        KeyboardButton(text="E"),
    )
    builder.row(
        KeyboardButton(text="Отмена"),
        KeyboardButton(text="Сбросить"),
    )
    return builder.as_markup(resize_keyboard=True)
