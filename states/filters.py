from aiogram.fsm.state import State, StatesGroup


class FiltersState(StatesGroup):
    select_filter = State()
    select_name = State()
    select_age = State()
    select_gender = State()
    select_education = State()
    select_region = State()
    select_profession = State()
    select_experience = State()
    select_type_of_employment = State()
    select_info = State()
    select_knowledge_of_languages = State()
    select_driving_license_category = State()
    select_own_car = State()
    select_citizenship = State()
    select_context = State()
