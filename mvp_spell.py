# from dnd_player_helper.dnd_model.dnd_model import DNDModel
import os
from dotenv import load_dotenv
from dnd_player_helper.mongo_model.dnd_model import DnDModel
from dnd_player_helper.spell_view import SpellView
from dnd_player_helper.spell_presenter import SpellPresenter
import flet as ft


def main():
    # load environment
    load_dotenv('.env')

    view = SpellView()
    uri = f"mongodb+srv://{os.environ.get("MONGODB_USER")}:{os.environ.get("MONGODB_PWD")}@cluster69.cipqchr.mongodb.net/?appName=Cluster69"
    model = DnDModel(uri=uri, db_name="session_zero")
    presenter = SpellPresenter(view=view, model=model)
    view.spell_presenter = presenter
    ft.app(
        target=view.create_ui,
        view=ft.WEB_BROWSER,
        assets_dir="assets",
    )

if __name__ == "__main__":
    main()
