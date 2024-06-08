import logging
from typing import Any, Protocol

# from dnd_player_helper.dnd_model.spell import Spell

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# add formatter to console_handler
console_handler.setFormatter(formatter)

# add console_handler to logger
logger.addHandler(console_handler)


class SpellView(Protocol):
    def set_name(self, name: str) -> None:
        ...

    def set_level(self, level: int) -> None:
        ...

    def set_spell_options(self, options: list[tuple[int, str]]) -> None:
        ...

    def set_entries(self, entries: list[dict[str, Any]]) -> None:
        ...

    def set_header(self, name: str, level: int, school: str, cast_time: str) -> None:
        ...


class DNDModel(Protocol):
    def get_spell_by_id(self, spell_id: int) -> str:
        ...

    def get_spell_ids_and_names(self) -> list[tuple[int, str]]:
        ...

    def get_entries_by_spell_id(self, spell_id: int) -> list[dict[str, Any]]:
        ...


class SpellPresenter:
    def __init__(self, view: SpellView, model: DNDModel) -> None:
        self.view = view
        self.model = model

    def update_spell_view(self, spell_id: int) -> None:
        spell_dict = self.model.get_spell_by_id(spell_id=spell_id)
        level = spell_dict.get("level")
        cast_times = spell_dict.get("spell_cast_times")
        if cast_times:
            logger.debug(f"cast_times: {cast_times}")
            cast_times = " or ".join(cast_times)
            logger.debug(f"cast_times: {cast_times}")

        spell_components = spell_dict.get("components")
        if spell_components:
            logger.debug(f"cast_times: {spell_components}")
            spell_components = ", ".join(spell_components)
            logger.debug(f"cast_times: {spell_components}")

        spell_durations = spell_dict.get("durations")
        if spell_durations:
            logger.debug(f"spell_durations: {spell_durations}")
            spell_durations = " or ".join(spell_durations)
            logger.debug(f"spell_durations: {spell_durations}")

        self.view.set_header(
            name=spell_dict.get("name"),
            level=level if level > 0 else "Cantrip",
            school=spell_dict.get("school"),
            cast_time=cast_times,
            spell_range=spell_dict.get("spell_range"),
            spell_components=spell_components,
            spell_duration=spell_durations,
        )

    def update_spell_options(self) -> None:
        options = self.model.get_spell_ids_and_names()
        self.view.set_spell_options(options)

    def update_entries_by_spell_id(self, spell_id: int) -> None:
        logger.debug(f"updating entries for spell_id: {spell_id}")
        entries = self.model.get_entries_by_spell_id(spell_id=spell_id)
        logger.debug(f"entry_set: {entries}")
        self.view.set_entries(entries=entries)
