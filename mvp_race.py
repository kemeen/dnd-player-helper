from dnd_player_helper.race_presenter import RacePresenter
from dnd_player_helper.race_view import RaceView
from dnd_player_helper.dnd_model.dnd_model import DNDModel
import flet as ft


def main():
    view = RaceView()
    model = DNDModel(echo=False)
    presenter = RacePresenter(view=view, model=model)
    view.race_presenter = presenter
    ft.app(
        target=view.create_ui,
        view=ft.WEB_BROWSER,
        assets_dir="assets",
    )


if __name__ == "__main__":
    main()
