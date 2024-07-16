# from dnd_player_helper.dnd_model.dnd_model import DNDModel
from dnd_player_helper.mongo_model.dnd_model import DnDModel
from dnd_player_helper.spell_view import SpellView
from dnd_player_helper.spell_presenter import SpellPresenter
import flet as ft


def main():
    view = SpellView()
    model = DnDModel(uri="mongodb://localhost:27017", db_name="session_zero")
    presenter = SpellPresenter(view=view, model=model)
    view.spell_presenter = presenter
    ft.app(
        target=view.create_ui,
        view=ft.WEB_BROWSER,
        assets_dir="assets",
    )

if __name__ == "__main__":
    main()
