from typing import Protocol


class HelloWorldModule(Protocol):
    text: str


class TranslatedText(Protocol):
    @property
    def hello_world(self) -> HelloWorldModule: ...
