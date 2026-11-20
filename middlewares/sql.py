from typing import Callable, Dict, Any, Awaitable

import aiomysql
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from data.config import settings


async def get_pool() -> aiomysql.Pool:
    return await aiomysql.create_pool(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        db="resume-analysis",
        autocommit=True,
        minsize=1,
        maxsize=10,
    )


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, pool: aiomysql.Pool):
        self.pool = pool

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        async with self.pool.acquire() as conn:
            # Кладём соединение в data под именем 'conn'
            data["conn"] = conn
            return await handler(event, data)
