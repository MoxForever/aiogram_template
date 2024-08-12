from aiogram import Router, types
from aiogram_dialog import DialogManager, StartMode

from ..dialogs import HelloWorldState

router = Router()


@router.message()
async def hello_world(_: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(HelloWorldState.hello_world, mode=StartMode.RESET_STACK)
