from dataclasses import dataclass
from typing import Optional


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
