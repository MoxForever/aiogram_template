from typing import Any
from aiogram import BaseMiddleware, types

from ...database import DAO, DatabaseConnection


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    async def __call__(
        self, handler, event: types.TelegramObject, data: dict[str, Any]
    ):
        async with DAO(self.db_connection) as dao:
            data["dao"] = dao
            return await handler(event, data)
