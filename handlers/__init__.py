"""Collects all routers into a single root router.
"""
from __future__ import annotations

from aiogram import Router

from . import channels, errors, groups
from .users import callbacks, echo, help, start, load_document, find, select_filter, apply_filter


def setup_routers() -> Router:
    router = Router(name="main")
    router.include_routers(
        start.router,
        help.router,
        callbacks.router,
        groups.router,
        channels.router,
        errors.router,
        load_document.router,
        find.router,
        select_filter.router,
        apply_filter.router,
        echo.router,
    )
    return router
