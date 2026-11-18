from typing import Optional


class Resume:
    """Resume class
    Attributes:
        document_url: Resume document_url
        name: Resume name
        age: Resume age
        gender: Resume gender
        education: Resume education
        region: Resume region
        profession: Resume profession
        experience: Resume experience
        type_of_employment: Resume type_of_employment
        info: Resume information
        knowledge_of_languages: Resume knowledge_of_languages
        driving_license_category: Resume driving_license_category
        own_car: Resume own_car
        citizenship: Resume citizenship
        """

    def __init__(self, document_url: str):
        self.document_url = document_url
        self.name: Optional[str] = None
        self.age: Optional[int] = None
        self.gender: Optional[str] = None
        self.education: Optional[list[str]] = None
        self.region: Optional[str] = None
        self.profession: Optional[str] = None
        self.experience: Optional[int] = None
        self.type_of_employment: Optional[str] = None
        self.info: Optional[str] = None
        self.knowledge_of_languages: Optional[list[dict[str, str]]] = None
        self.driving_license_category: Optional[str] = None
        self.own_car: Optional[str] = None
        self.citizenship: Optional[str] = None

    def __str__(self):
        return str(self.__dict__)
