import asyncio
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject


class MediaGroupMiddleware(BaseMiddleware):
    def __init__(self, latency: float = 0.1) -> None:
        self.medias: dict[str, list[Message]] = {}
        self.latency = latency

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        if isinstance(event, Message) and event.media_group_id:
            group_id = event.media_group_id

            if group_id in self.medias:
                self.medias[group_id].append(event)
                return

            self.medias[group_id] = [event]
            await asyncio.sleep(self.latency)
            media_events = self.medias.pop(group_id)
            data["media_events"] = media_events
            return await handler(event, data)

        return await handler(event, data)
