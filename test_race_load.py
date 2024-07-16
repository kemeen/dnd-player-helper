import pathlib
from dnd_player_helper.race import load_race

DATA_PATH = r"C:\software_projects\python\dnd-player-helper\data\race"


def main():
    path = pathlib.Path(DATA_PATH)
    for json_file in path.glob("*.json"):
        race = load_race(json_file)
        print(
            race.name,
            race.speed,
            race.darkvision,
            # race.trait_tags,
            # race.ability_modifier,
        )


if __name__ == "__main__":
    main()
