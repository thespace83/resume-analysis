from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.default import apply_filters_keyboard
from states import FiltersState


async def activate_name_filters(
        message: Message,
        state: FSMContext,
) -> None:
    await state.set_state(FiltersState.select_name)
    await message.answer(
        "Введите имя или часть имени кандидата",
        reply_markup=apply_filters_keyboard()
    )


async def activate_profession_filters(
        message: Message,
        state: FSMContext,
) -> None:
    await state.set_state(FiltersState.select_profession)
    await message.answer(
        "Введите название или часть названия профессии кандидата",
        reply_markup=apply_filters_keyboard()
    )

#
# async def activate_age_filters(
#         message: Message,
#         state: FSMContext,
# ) -> None:
#     await state.set_state(FiltersState.select_name)
#     await message.answer(
#         "Введите возраст кандидата",
#         reply_markup=get_select_filter_keyboard()
#     )
#
#
# async def activate_gender_filters(
#         message: Message,
#         state: FSMContext,
# ) -> None:
#     await state.set_state(FiltersState.select_name)
#     await message.answer(
#         "Выберите гендер кандидата",
#         reply_markup=get_select_filter_keyboard()
#     )
#
#
# async def activate_education_filters(
#         message: Message,
#         state: FSMContext,
# ) -> None:
#     await state.set_state(FiltersState.select_name)
#     await message.answer(
#         "Выберите образование кандидата",
#         reply_markup=get_select_filter_keyboard()
#     )
#
#
# async def activate_region_filters(
#         message: Message,
#         state: FSMContext,
# ) -> None:
#     await state.set_state(FiltersState.select_name)
#     await message.answer(
#         "Введите регион работы кандидата",
#         reply_markup=get_select_filter_keyboard()
#     )
#
#
# async def activate_profession_filters(
#         message: Message,
#         state: FSMContext,
# ) -> None:
#     await state.set_state(FiltersState.select_name)
#     await message.answer(
#         "Введите профессию кандидата",
#         reply_markup=get_select_filter_keyboard()
#     )
#
#
# async def activate_experience_filters(
#         message: Message,
#         state: FSMContext,
# ) -> None:
#     await state.set_state(FiltersState.select_name)
#     await message.answer(
#         "Введите опыт работы кандидата",
#         reply_markup=get_select_filter_keyboard()
#     )
