from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from fastapi import FastAPI
from fastapi.middleware import Middleware

from ..settings import Settings
from ..database import DatabaseConnection
from .middlewares import DatabaseMiddleware
from .routers import telegram_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    bot: Bot = app.state.bot
    dp: Dispatcher = app.state.dp
    workflow_data = {"app": app, "dispatcher": dp, **dp.workflow_data}

    settings = Settings()
    if settings.TELEGRAM_WEBHOOK_URL:
        await bot.set_webhook(
            url=settings.TELEGRAM_WEBHOOK_URL,
            secret_token=settings.TELEGRAM_SECRET_TOKEN,
        )

    await dp.emit_startup(**workflow_data)

    yield

    await dp.emit_shutdown(**workflow_data)


def setup_web_app(
    db_connection: DatabaseConnection, dp: Dispatcher, bot: Bot
) -> FastAPI:
    middleware = [
        # Middleware(DatabaseMiddleware, db_connection=db_connection),
    ]

    app = FastAPI(middleware=middleware, lifespan=lifespan)

    app.state.bot = bot
    app.state.dp = dp

    app.include_router(telegram_router)

    return app
