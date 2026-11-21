from dataclasses import dataclass
from enum import Enum
from typing import Optional


class FilterTypes(Enum):
    NAME = 0,
    AGE = 1,
    GENDER = 2,
    EDUCATION = 3,
    REGION = 4,
    PROFESSION = 5,
    EXPERIENCE = 6,
    TYPE_OF_EMPLOYMENT = 7,
    INFO = 8,
    KNOWLEDGE_OF_LANGUAGES = 9,
    DRIVING_LICENSE_CATEGORY = 10,
    OWN_CAR = 11,
    CITIZENSHIP = 12,
    CONTEXT = 13


@dataclass
class Resume:
    document_url: str
    name: Optional[str]
    age: Optional[int]
    gender: Optional[str]
    education: Optional[str]
    region: Optional[str]
    profession: Optional[str]
    experience: Optional[int]
    type_of_employment: Optional[str]
    info: Optional[str]
    knowledge_of_languages: Optional[list[dict[str, str]]]
    driving_license_category: Optional[str]
    own_car: Optional[str]
    citizenship: Optional[str]
    context: str

    def __str__(self):
        return str(__dict__)
