from os import name
import pathlib
from typing import Protocol, Self
from dnd_player_helper.race import Race, load_race
from dnd_player_helper.dnd_model.dnd_class import DNDClass, load_class
from dnd_player_helper.dnd_model.race import (
    Race as DNDRace,
    RaceAge,
    RaceDescriptions,
    RaceWeaponProficiency,
)


class View(Protocol):
    def update_name(self, name: str) -> None:
        ...

    def get_name(self) -> str:
        ...

    def update_class_name(self, class_name: str) -> None:
        ...

    def get_class_name(self) -> str:
        ...

    def update_level(self, level: int) -> None:
        ...

    def get_level(self) -> int:
        ...

    def update_character_list(self, character_list: list[str]) -> None:
        ...

    def get_race(self) -> str:
        ...

    def update_race(self, race: str) -> None:
        ...


class Model(Protocol):
    def update_name(self, name: str) -> None:
        ...

    def get_name(self) -> str:
        ...

    def update_class(self, class_name: str) -> None:
        ...

    def get_class(self) -> str:
        ...

    def update_race(self, race: str) -> None:
        ...

    def get_race(self) -> str:
        ...

    def update_level(self, level: int) -> None:
        ...

    def get_level(self) -> int:
        ...

    def run(self) -> None:
        ...

    def dump(self, file_name: str) -> None:
        ...

    def load(self, file_name: str) -> None:
        ...


class DNDModel(Protocol):
    def get_all_races() -> list[DNDRace]:
        ...

    def get_race_by_id(self, race_id: int) -> Race:
        ...

    def get_race_age_by_race_id(self, race_id: int) -> list[RaceAge]:
        ...

    def get_weapon_proficiency_by_race_id(
        self, race_id: int
    ) -> list[RaceWeaponProficiency]:
        ...

    def get_descriptions_by_race_id(self, race_id: int) -> list[RaceDescriptions]:
        ...


class CharacterPresenter:
    def __init__(self, view: View, model: Model) -> None:
        self.view = view
        self.model = model
        self.update_character_list()
        self.races = dict()
        self.classes = dict()

    def handle_name_update(self, event=None) -> None:
        name = self.view.get_name()
        self.model.update_name(name)
        self.view.update_name(self.model.get_name())

    def handle_class_update(self, event=None) -> None:
        class_name = self.view.get_class_name()
        self.model.update_class(class_name)
        self.view.update_class_name(self.model.get_class())

    def handle_level_update(self, event=None) -> None:
        level = self.view.get_level()
        self.model.update_level(level)
        self.view.update_level(self.model.get_level())

    def handle_race_update(self, event=None) -> None:
        race = self.view.get_race()
        self.model.update_race(race=race)
        self.view.update_race(self.model.get_race())

    def get_character_name(self) -> str:
        return self.model.get_name()

    def get_character_class(self) -> str:
        return self.model.get_class()

    def get_character_level(self) -> str:
        return self.model.get_level()

    def get_race(self) -> str:
        return self.model.get_race()

    def save_character(self, file_name: str) -> None:
        file_name = file_name.replace(" ", "_")
        self.model.dump(f"{file_name}.json")
        self.update_character_list()

    def load_character(self, file_name: str) -> None:
        file_name = file_name.replace(" ", "_")
        self.model.load(f"{file_name}.json")
        self.update_view()

    def update_view(self) -> None:
        self.view.update_name(self.model.get_name())
        self.view.update_class_name(self.model.get_class())
        self.view.update_level(self.model.get_level())
        self.view.update_race(self.model.get_race())

    def update_character_list(self) -> None:
        characters = [f.stem for f in pathlib.Path(".").glob("*.json")]
        print(characters)
        self.view.update_character_list(characters)

    def load_races(self, data_path: str) -> None:
        path = pathlib.Path(data_path)
        for json_file in path.glob("*.json"):
            race = load_race(str(json_file))
            self.races[race.name] = race

    def load_classes(self, data_path: str) -> None:
        path = pathlib.Path(data_path)
        for json_file in path.glob("*.json"):
            dnd_class = load_class(str(json_file))
            # print("adding class", dnd_class.name)
            self.classes[dnd_class.name] = dnd_class

    def get_race_from_list(self, race_name: str) -> Race | None:
        return self.races.get(race_name)

    def get_class_from_list(self, class_name: str) -> DNDClass | None:
        return self.classes.get(class_name)

    def get_list_of_races(self) -> list[str]:
        return [race for race in self.races.keys()]

    def get_list_of_classes(self) -> list[str]:
        return [class_name for class_name in self.classes.keys()]

    def run(self):
        self.view.run()


class DNDPresenter:
    def __init__(self, view: View, dnd_model: DNDModel) -> None:
        self.view = view
        self.dnd_model = dnd_model
        # self.races = dict()
        # self.classes = dict()

    def load_races_from_db(self) -> list[DNDRace]:
        return self.dnd_model.get_all_races()

    def get_race_ids_and_names(self) -> list[tuple[int, str]]:
        return [
            (race.id, f"{race.name}-{race.source}")
            for race in self.load_races_from_db()
        ]

    def get_race_by_id(self, race_id: int) -> DNDRace:
        return self.dnd_model.get_race_by_id(race_id=race_id)

    def get_race_age_by_id(self, race_id: int) -> list[RaceAge]:
        return self.dnd_model.get_race_age_by_race_id(race_id=race_id)

    def get_race_weapon_proficiencies_by_id(
        self, race_id: int
    ) -> list[RaceWeaponProficiency]:
        return self.dnd_model.get_weapon_proficiency_by_race_id(race_id=race_id)

    def get_race_descriptions_by_id(self, race_id: int) -> list[RaceDescriptions]:
        return self.dnd_model.get_descriptions_by_race_id(race_id=race_id)
