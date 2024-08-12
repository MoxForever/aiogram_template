from aiogram_template import setup_web_app, setup_bot, setup_dispatcher
from aiogram_template.settings import Settings
from aiogram_template.database import DatabaseConnection


def app():
    settings = Settings()
    db_connection = DatabaseConnection(settings.DATABASE_POSTGRES_URL)

    bot = setup_bot(settings)
    dp = setup_dispatcher(settings, db_connection)

    return setup_web_app(db_connection, dp, bot)
