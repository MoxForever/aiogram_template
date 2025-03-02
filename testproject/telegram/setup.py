from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_dialog import setup_dialogs

from ..settings import Settings
from ..database import DatabaseConnection
from .dialogs import dialogs_router
from .routers import routers_group
from . import middlewares


def setup_bot(settings: Settings) -> Bot:
    return Bot(
        settings.TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML"),
        session=AiohttpSession(
            api=TelegramAPIServer.from_base(settings.TELEGRAM_API_URL)
        ),
    )


def setup_dispatcher(
    settings: Settings, db_connection: DatabaseConnection
) -> Dispatcher:
    dp = Dispatcher(
        storage=RedisStorage.from_url(
            settings.DATABASE_REDIS_URL,
            key_builder=DefaultKeyBuilder(with_destiny=True),
        )
    )

    database_middleware = middlewares.DatabaseMiddleware(db_connection)
    dp.update.middleware(database_middleware)

    translation_middleware = middlewares.TranslationMiddleware()
    dp.message.middleware(translation_middleware)
    dp.callback_query.middleware(translation_middleware)

    setup_dialogs(dp)
    dp.include_routers(
        dialogs_router,
        routers_group,
    )

    return dp
