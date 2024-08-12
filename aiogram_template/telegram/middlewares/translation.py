from typing import Any
from aiogram import BaseMiddleware, types

from ...translation import languages_dict


class TranslationMiddleware(BaseMiddleware):
    async def __call__(
        self, handler, event: types.Message | types.CallbackQuery, data: dict[str, Any]
    ):
        lang = event.from_user.language_code or "en"
        data["tr"] = languages_dict[lang]
        return await handler(event, data)
