import json


class Model:
    def __init__(self) -> None:
        self.name = ""
        self.class_name = ""
        self.race = ""
        self.level = 0

    def update_name(self, name: str) -> None:
        self.name = name

    def get_name(self) -> str:
        return self.name

    def update_class(self, class_name: str) -> None:
        self.class_name = class_name

    def get_class(self) -> str:
        return self.class_name

    def update_race(self, race: str) -> None:
        self.race = race

    def get_race(self) -> str:
        return self.race

    def update_level(self, level: int) -> None:
        self.level = level

    def get_level(self) -> int:
        return self.level

    def dump(self, file_name: str) -> None:
        print(f"saving character {self.name} to {file_name}")
        with open(file_name, "w") as f:
            json.dump(self.__dict__, f)

    def load(self, file_name: str) -> None:
        print(f"loading character from {file_name}")
        with open(file_name, "r") as f:
            self.__dict__.update(json.load(f))
