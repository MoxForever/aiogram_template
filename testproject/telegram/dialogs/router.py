from aiogram import Router

from .hello_world import hello_world_dialog

dialogs_router = Router()

dialogs_router.include_routers(
    hello_world_dialog,
    # TODO add dialogs
)
