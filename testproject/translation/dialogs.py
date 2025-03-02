from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import true_condition
from aiogram_dialog.widgets.text import Text
from aiogram_dialog.widgets.text.format import _FormatDataStub

from .protocol import TranslatedText
from .langs import ru, en


class _DialogLocalizationPath(Text):
    def __init__(self, full_path: list[str]):
        self.condition = true_condition  # type: ignore
        self.full_path = full_path

    def __getattr__(self, name: str) -> "_DialogLocalizationPath":
        return _DialogLocalizationPath(self.full_path + [name])

    async def _render_text(self, data, manager: DialogManager) -> str:
        tr = manager.middleware_data["tr"]
        for name in self.full_path:
            tr = getattr(tr, name)

        if manager.is_preview():
            return tr.format_map(_FormatDataStub(data=data))
        return tr.format_map(data)


DialogLocalization: TranslatedText = _DialogLocalizationPath([])  # type: ignore


languages_dict: dict[str, TranslatedText] = {
    "ru": ru,
    "en": en,
}
