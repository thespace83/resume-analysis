resume_format = {
    "format": {
        "type": "json_schema",
        "name": "resume_response",
        "schema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                },
                "age": {
                    "type": "integer",
                },
                "gender": {
                    "type": "string",
                    "enum": ["мужчина", "женщина", ""],
                },
                "education": {
                    "type": "string",
                    "enum": [
                        "среднее", "средне специальное", "неоконченное высшее",
                        "высшее", "бакалавриат", "магистратура",
                        "кандидат наук", "доктор наук", "прочее", ""]
                },
                "region": {
                    "type": "string",
                },
                "profession": {
                    "type": "string",
                },
                "experience": {
                    "type": "integer",
                },
                "type-of-employment": {
                    "type": "string",
                    "enum": ["постоянная работа", "подработка", "стажировка", "прочее", ""],
                },
                "info": {
                    "type": "string"
                },
                "knowledge-of-languages": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "language": {"type": "string"},
                            "level": {
                                "type": "string",
                                "enum": ["A1", "A2", "B1", "B2", "C1", "C2", "родной"]
                            }
                        },
                        "required": ["language", "level"],
                        "additionalProperties": False
                    }
                },
                "driving-license-category": {
                    "type": "string",
                    "enum": ["А", "В", "С", "D", "E", ""],
                },
                "own-car": {
                    "type": "string",
                    "enum": ["да", "нет", ""],
                },
                "citizenship": {
                    "type": "string"
                },
            },
            "required": [
                "name", "age", "gender", "education", "region", "profession",
                "experience", "type-of-employment", "info", "knowledge-of-languages",
                "driving-license-category", "own-car", "citizenship",
            ],
            "strict": True,
            "additionalProperties": False,
        }
    }
}
