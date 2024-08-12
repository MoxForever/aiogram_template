from aiogram.fsm.state import State, StatesGroup


class HelloWorldState(StatesGroup):
    hello_world = State()
