from aiogram import Bot, Dispatcher, types
from aiogram.methods import TelegramMethod
from fastapi import APIRouter, HTTPException, Request

from ...settings import Settings


telegram_router = APIRouter(prefix=Settings().TELEGRAM_WEBHOOK_PATH)

@telegram_router.post("")
async def telegram(request: Request):
    settings = Settings()

    if settings.TELEGRAM_SECRET_TOKEN:
        header_secret_token: str | None = request.headers.get(
            "X-Telegram-Bot-Api-Secret-Token"
        )
        if settings.TELEGRAM_SECRET_TOKEN != header_secret_token:
            raise HTTPException(status_code=400, detail="Secret token incorrect")

    dp: Dispatcher = request.app.state.dp
    bot: Bot = request.app.state.bot
    update = types.Update(**await request.json())

    result = await dp.feed_webhook_update(bot, update)
    if isinstance(result, TelegramMethod):
        await dp.silent_call_request(bot=bot, result=result)
