import aiomysql
from models.resume import Resume


def get_where_clause(name=None, age=None, gender=None, education=None, region=None,
                     profession=None, experience=None, type_of_employment=None,
                     info=None, knowledge_of_languages=None,
                     driving_license_category=None, own_car=None, citizenship=None,
                     context=None) -> tuple[str, list]:
    filters = []
    params = []

    int_fields = {
        "age": age,
        "experience": experience,
    }
    for column, value in int_fields.items():
        if value is not None:
            symbol = value[0]
            number = value[1:]
            filters.append(f"{column} {symbol}{"=" if symbol != "=" else ""} %s")
            params.append(number)

    exact_fields = {
        "gender": gender,
        "own_car": own_car,
    }
    for column, value in exact_fields.items():
        if value is not None:
            filters.append(f"{column} = %s")
            params.append(value)

    like_fields = {
        "name": name,
        "profession": profession,
        "info": info,
        "education": education,
        "region": region,
        "type_of_employment": type_of_employment,
        "citizenship": citizenship,
        "driving_license_category": driving_license_category,
    }
    for column, value in like_fields.items():
        if value is not None:
            filters.append(f"{column} LIKE %s")
            params.append(f"%{value}%")

    return ("WHERE " + " AND ".join(filters)) if filters else "", params


def search_resumes(
        name=None, age=None, gender=None, education=None, region=None,
        profession=None, experience=None, type_of_employment=None,
        info=None, knowledge_of_languages=None,
        driving_license_category=None, own_car=None, citizenship=None,
        context=None, limit=20, offset=0,
):
    where_clause, params = get_where_clause(name=name, age=age, gender=gender, education=education, region=region,
                                            profession=profession, experience=experience,
                                            type_of_employment=type_of_employment,
                                            info=info, knowledge_of_languages=knowledge_of_languages,
                                            driving_license_category=driving_license_category, own_car=own_car,
                                            citizenship=citizenship,
                                            context=context)
    query = f"""
        SELECT id, document_url, name, age, gender, education, region,
               profession, experience, type_of_employment, info,
               driving_license_category, own_car, citizenship, context
        FROM resumes
        {where_clause}
        ORDER BY id
        LIMIT %s OFFSET %s
    """
    params.extend([limit, offset])
    return query, params


def search_count_of_resumes(
        name=None, age=None, gender=None, education=None, region=None,
        profession=None, experience=None, type_of_employment=None,
        info=None, knowledge_of_languages=None,
        driving_license_category=None, own_car=None, citizenship=None,
        context=None
):
    where_clause, params = get_where_clause(name=name, age=age, gender=gender, education=education, region=region,
                                            profession=profession, experience=experience,
                                            type_of_employment=type_of_employment,
                                            info=info, knowledge_of_languages=knowledge_of_languages,
                                            driving_license_category=driving_license_category, own_car=own_car,
                                            citizenship=citizenship,
                                            context=context)

    query = f"""
        SELECT COUNT(*)
        FROM resumes
        {where_clause}
    """
    return query, params


class ResumesRepository:
    def __init__(self, pool: aiomysql.Pool):
        self.pool = pool

    async def create(self, resume: Resume) -> int:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "INSERT INTO resumes (`document_url`, `name`, `age`, `gender`, `education`, `region`, `profession`, `experience`, `type_of_employment`, `info`, `driving_license_category`, `own_car`, `citizenship`, `context`) " +
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (resume.document_url, resume.name, resume.age, resume.gender, resume.education, resume.region,
                     resume.profession, resume.experience, resume.type_of_employment, resume.info,
                     resume.driving_license_category, resume.own_car, resume.citizenship, resume.context)
                )
                resume_id = cur.lastrowid
                if resume.knowledge_of_languages is not None:
                    for knowledge in resume.knowledge_of_languages:
                        await cur.execute(
                            "INSERT INTO `knowledge-of-languages` (`resume_id`, `language`, `level`) " +
                            "VALUES (%s, %s, %s)",
                            (resume_id, knowledge['language'], knowledge['level'])
                        )
                return resume_id

    async def get_count_of_resumes(
            self,
            name=None,
            age=None,
            gender=None,
            education=None,
            region=None,
            profession=None,
            experience=None,
            type_of_employment=None,
            info=None,
            knowledge_of_languages=None,
            driving_license_category=None,
            own_car=None,
            citizenship=None,
            context=None,
    ) -> int:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                query, params = search_count_of_resumes(
                    name=name, age=age, gender=gender, education=education, region=region, profession=profession,
                    experience=experience, type_of_employment=type_of_employment, info=info,
                    knowledge_of_languages=knowledge_of_languages, driving_license_category=driving_license_category,
                    own_car=own_car, citizenship=citizenship, context=context
                )
                await cur.execute(query, params)
                row = await cur.fetchone()
                return row[0]

    async def get_resumes(
            self,
            limit: int,
            offset: int,
            name=None,
            age=None,
            gender=None,
            education=None,
            region=None,
            profession=None,
            experience=None,
            type_of_employment=None,
            info=None,
            knowledge_of_languages=None,
            driving_license_category=None,
            own_car=None,
            citizenship=None,
            context=None,
    ) -> dict[int, Resume]:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                query, params = search_resumes(
                    limit=limit, offset=offset, name=name, age=age, gender=gender, education=education, region=region,
                    profession=profession, experience=experience, type_of_employment=type_of_employment, info=info,
                    knowledge_of_languages=knowledge_of_languages, driving_license_category=driving_license_category,
                    own_car=own_car, citizenship=citizenship, context=context
                )
                await cur.execute(query, params)
                rows = await cur.fetchall()
                resumes = {}
                for row in rows:
                    resumes[row[0]] = Resume(
                        document_url=row[1],
                        name=row[2],
                        age=row[3],
                        gender=row[4],
                        education=row[5],
                        region=row[6],
                        profession=row[7],
                        experience=row[8],
                        type_of_employment=row[9],
                        info=row[10],
                        knowledge_of_languages=None,
                        driving_license_category=row[11],
                        own_car=row[12],
                        citizenship=row[13],
                        context=row[14]
                    )
                return resumes

    async def get_resume(self, number: int) -> Resume | None:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """
                    SELECT *
                    FROM resumes
                    WHERE id = %s;
                    """,
                    (number,),
                )
                rows = await cur.fetchall()
                if len(rows) == 0:
                    return None
                row = rows[0]

                resume = Resume(
                    document_url=row[1],
                    name=row[2],
                    age=row[3],
                    gender=row[4],
                    education=row[5],
                    region=row[6],
                    profession=row[7],
                    experience=row[8],
                    type_of_employment=row[9],
                    info=row[10],
                    knowledge_of_languages=None,
                    driving_license_category=row[11],
                    own_car=row[12],
                    citizenship=row[13],
                    context=row[14]
                )

                await cur.execute(
                    """
                    SELECT *
                    FROM `knowledge-of-languages`
                    WHERE resume_id = %s;
                    """,
                    (number,),
                )

                rows = await cur.fetchall()
                knowledge_of_languages = []
                for row in rows:
                    knowledge_of_languages.append({
                        "language": row[1],
                        "level": row[2]
                    })
                resume.knowledge_of_languages = knowledge_of_languages

                return resume

    async def get_document_id(self, number: int) -> str:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """
                    SELECT document_url
                    FROM resumes
                    WHERE id = %s;
                    """,
                    (number,),
                )
                row = await cur.fetchall()
                return row[0][0]

    # async def get_by_user(self, user_id: int) -> list[Resume]:
    #     async with self.pool.acquire() as conn:
    #         async with conn.cursor(aiomysql.DictCursor) as cur:
    #             await cur.execute(
    #                 "SELECT id, user_id, text, created_at FROM notes WHERE user_id = %s ORDER BY created_at DESC",
    #                 (user_id,)
    #             )
    #             rows = await cur.fetchall()
    #             return [Note(**row) for row in rows]

    # async def delete(self, note_id: int, user_id: int) -> bool:
    #     """Удаляет заметку, только если она принадлежит пользователю."""
    #     async with self.pool.acquire() as conn:
    #         async with conn.cursor() as cur:
    #             await cur.execute(
    #                 "DELETE FROM notes WHERE id = %s AND user_id = %s",
    #                 (note_id, user_id)
    #             )
    #             return cur.rowcount > 0
