import pathlib
from dnd_player_helper.color_theme import import_color_theme
from dnd_player_helper.model import Model
from dnd_player_helper.presenter import CharacterPresenter, DNDPresenter
from dnd_player_helper.view import CharacterView
from dnd_player_helper.dnd_model.dnd_model import DNDModel
import flet as ft

CHARACTER_FILE = r"morgan.json"
RACES_DATA_PATH = r"C:\software_projects\python\dnd-player-helper\data\race"
CLASSES_DATA_PATH = r"C:\software_projects\python\dnd-player-helper\data\class"


def main():
    character_model = Model()
    character_file = pathlib.Path(CHARACTER_FILE)
    if character_file.exists():
        character_model.load(CHARACTER_FILE)
    view = CharacterView()
    character_presenter = CharacterPresenter(view, character_model)

    dnd_model = DNDModel()
    dnd_presenter = DNDPresenter(view=view, dnd_model=dnd_model)

    # presenter.load_races(data_path=RACES_DATA_PATH)
    # presenter.load_classes(data_path=CLASSES_DATA_PATH)
    # print(presenter.classes.keys())
    view.character_presenter = character_presenter
    view.dnd_presenter = dnd_presenter
    # presenter.run()
    ft.app(target=view.create_ui, view=ft.WEB_BROWSER)


if __name__ == "__main__":
    main()
