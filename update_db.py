import pathlib

from dnd_player_helper.dnd_model.dnd_model import DNDModel


RACES_DATA_PATH = pathlib.Path(
    r"C:\software_projects\python\dnd-player-helper\data\race"
)
SKILL_DATA_PATH = pathlib.Path(
    r"C:\software_projects\python\dnd-player-helper\data\skill"
)
LANGUAGE_DATA_PATH = pathlib.Path(
    r"C:\software_projects\python\dnd-player-helper\data\language"
)
ALL_LANGUAGES_DATA_PATH = pathlib.Path(
    r"C:\software_projects\python\dnd-player-helper\data\language\all_languages.json"
)


def main() -> None:
    model = DNDModel(echo=False)
    model.delete_db()
    model.create_db_and_tables()
    model.add_damage_types(
        data_path=pathlib.Path(
            r"C:\software_projects\python\dnd-player-helper\data\tables\damage_types.json"
        )
    )
    model.add_item_properties(
        data_path=pathlib.Path(
            r"C:\software_projects\python\dnd-player-helper\data\items\base\itemProperty"
        )
    )
    model.add_item_types(
        data_path=pathlib.Path(
            r"C:\software_projects\python\dnd-player-helper\data\items\base\itemType"
        )
    )
    model.add_items(
        data_path=pathlib.Path(
            r"C:\software_projects\python\dnd-player-helper\data\items\base\baseitem"
        )
    )
    # model.add_language_table(data_path=ALL_LANGUAGES_DATA_PATH)
    # model.add_skill_table(data_path=SKILL_DATA_PATH)
    # model.add_size_table(data_path=None)
    # model.add_race_tables(data_path=RACES_DATA_PATH)


if __name__ == "__main__":
    main()
