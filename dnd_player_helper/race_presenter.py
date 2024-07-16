import logging
from typing import Any, Protocol

from dnd_player_helper.dnd_model.race import Race

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


class RaceView(Protocol):
    def set_name(self, name: str) -> None:
        ...

    def set_age(self, ages: dict[str, int]) -> None:
        ...

    def set_size(self, size: str) -> None:
        ...

    def set_weapon_proficiencies(self, weapon_proficiencies: list[str]) -> None:
        ...

    def set_race_options(self, options: list[tuple[int, str]]) -> None:
        ...

    def set_entries(self, entry_set_dict: dict[str, Any]) -> None:
        ...


class DNDModel(Protocol):
    def get_race_name_by_race_id(self, race_id: int) -> str:
        ...

    def get_race_sizes_by_race_id(self, race_id: int) -> list[str]:
        ...

    def get_race_ages_by_race_id(self, race_id: int) -> dict[str, int]:
        ...

    def get_race_weapon_proficiencies_by_race_id(self, race_id: int) -> list[str]:
        ...

    def get_race_ids_and_names(self) -> list[tuple[int, str]]:
        ...

    def get_race_entries_by_race_id(self, race_id: int) -> list[dict[str, str]]:
        ...


class RacePresenter:
    def __init__(self, view: RaceView, model: DNDModel) -> None:
        self.view = view
        self.model = model

    def update_weapon_proficiencies_by_id(self, race_id: int) -> None:
        weapon_proficiencies = self.model.get_race_weapon_proficiencies_by_race_id(
            race_id=race_id
        )
        self.view.set_weapon_proficiencies(weapon_proficiencies)

    def update_name_by_id(self, race_id: int) -> None:
        name = self.model.get_race_name_by_race_id(race_id=race_id)
        self.view.set_name(name)

    def update_size_by_id(self, race_id: int) -> None:
        sizes = self.model.get_race_sizes_by_race_id(race_id=race_id)
        size_string = ", ".join(sizes)

        self.view.set_size(size_string)

    def update_age_by_id(self, race_id: int) -> None:
        ages = self.model.get_race_ages_by_race_id(race_id=race_id)
        self.view.set_age(ages)

    def update_race_options(self) -> None:
        options = self.model.get_race_ids_and_names()
        self.view.set_race_options(options)

    def update_entries_by_race_id(self, race_id: int) -> None:
        entry_set = self.model.get_race_entries_by_race_id(race_id=race_id)
        self.view.set_entries(entry_set)
