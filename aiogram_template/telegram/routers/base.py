from aiogram import Router

from . import hello_world

routers_group = Router()

routers_group.include_routers(
    hello_world.router,
    # TODO add routers
)
