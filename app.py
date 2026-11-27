"""Bot entry point."""
from __future__ import annotations

import asyncio
import logging
import sys

from aiogram.types import BotCommandScopeAllPrivateChats

from handlers import setup_routers
from loader import bot, dp
from middlewares.logging import LoggingMiddleware
from middlewares.media_group import MediaGroupMiddleware
from middlewares.sql import DbSessionMiddleware, get_pool
from utils.notify_admins import on_shutdown, on_startup
from utils.set_botcommands import commands


async def main() -> None:
    dp.message.middleware(LoggingMiddleware())
    dp.message.middleware(MediaGroupMiddleware(latency=0.1))
    dp.message.middleware(DbSessionMiddleware(await get_pool()))
    dp.include_router(setup_routers())
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)


    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands, scope=BotCommandScopeAllPrivateChats())

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("app.log", mode="a", encoding="utf-8"),
        ],
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    asyncio.run(main())
