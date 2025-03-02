from aiogram_dialog import Window

from aiogram_template.translation import DialogLocalization

from ..state import HelloWorldState


hello_world_window = Window(
    DialogLocalization.hello_world.text,
    state=HelloWorldState.hello_world,
)
