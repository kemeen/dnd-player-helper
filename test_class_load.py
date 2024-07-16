import pathlib
from dnd_player_helper.dnd_model.dnd_class import DNDClass, load_class

DATA_PATH = r"C:\software_projects\python\dnd-player-helper\data\class"


def main():
    path = pathlib.Path(DATA_PATH)
    for json_file in path.glob("*.json"):
        dnd_class: DNDClass = load_class(json_file)
        print(
            dnd_class.name,
            dnd_class.features,
            # dnd_class.hit_die,
            # race.trait_tags,
            # race.ability_modifier,
        )
        break


if __name__ == "__main__":
    main()
