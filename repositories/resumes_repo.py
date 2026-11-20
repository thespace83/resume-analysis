import aiomysql
from models.resume import Resume


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
                return cur.lastrowid

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
