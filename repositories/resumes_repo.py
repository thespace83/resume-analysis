import aiomysql

from models.resume import Resume


class ResumesRepository:
    """Repository for working with resumes
    """

    def __init__(self, pool: aiomysql.Pool):
        self.pool = pool

    async def create(self, resume: Resume):
        """Create the entry
        """
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """
                    INSERT INTO resumes (`url`, `name`, `age`, `gender`, `education`, `region`, `profession`,
                                         `work_experience`, `type_of_employment`, `driving_license_category`, `own_car`,
                                         `citizenship`, `info`, `context`)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        resume.url,
                        resume.name,
                        resume.age,
                        resume.gender,
                        resume.education,
                        resume.region,
                        resume.profession,
                        resume.work_experience,
                        resume.type_of_employment,
                        resume.driving_license_category,
                        resume.own_car,
                        resume.citizenship,
                        resume.info,
                        resume.context,
                    ))
                return await cursor.fetchall()
