import copy
import logging
from turtle import title
from typing import Any, Optional, Protocol
import flet as ft
from dnd_player_helper.ui.entity import render_entry_set, render_list
from dnd_player_helper.ui.hero_section import HeroSectionImageRight
from dnd_player_helper.theme import text_theme

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

INSET = 4


class RacePresenter(Protocol):
    def update_weapon_proficiencies_by_id(self, race_id: int) -> None:
        ...

    def update_name_by_id(self, race_id: int) -> None:
        ...

    def update_size_by_id(self, race_id: int) -> None:
        ...

    def update_age_by_id(self, race_id: int) -> None:
        ...

    def update_entries_by_race_id(self, race_id: int) -> None:
        ...

    def update_race_options() -> None:
        ...


# class RaceSelector(ft.UserControl):
#     def __init__(self):
#         self.race_selection = ft.Dropdown(label="Race", hint_text="Select a Race")


class RaceView:
    def __init__(self):
        super().__init__()
        self.race_presenter: RacePresenter = None
        # self.race_id = race_id
        self.race_selection = ft.Dropdown(
            label="Race",
            hint_text="Select a Race",
            width=300,
        )
        self.name_control = ft.Text("", style=text_theme.title_large)
        self.size_control = ft.Text("", style=text_theme.display_small)
        self.age_control = ft.Text("", style=text_theme.display_small)
        self.weapon_proficiencies_control = ft.Column(spacing=0)
        self.entries_control = ft.Column(height=400, scroll=True, spacing=10)
        self.background = ft.colors.PRIMARY_CONTAINER

    def create_ui(self, page: ft.Page) -> None:
        # set theme
        page.fonts = {
            "Brush": "/fonts/BRUSHSCI.ttf",
            "BRLNSB": "/fonts/BRLNSB.ttf",
            "BRLNSDB": "/fonts/BRLNSDB.ttf",
            "BRLNSR": "/fonts/BRLNSR.ttf",
        }
        page.theme = ft.Theme(text_theme=text_theme)

        def on_race_change(event: ft.ControlEvent) -> None:
            # print(event.control)
            # print(event.control.value)
            race_id = event.control.value
            self.race_presenter.update_name_by_id(race_id=race_id)
            self.race_presenter.update_size_by_id(race_id=race_id)
            self.race_presenter.update_age_by_id(race_id=race_id)
            self.race_presenter.update_weapon_proficiencies_by_id(race_id=race_id)
            self.race_presenter.update_entries_by_race_id(race_id=race_id)
            page.update()

        # page.theme.text_theme = text_theme

        # add hero section
        hero_section = HeroSectionImageRight(
            image=ft.Image(
                src="images/hero_large.png",
                width=378,
                height=252,
                fit=ft.ImageFit.NONE,
                repeat=ft.ImageRepeat.NO_REPEAT,
            ),
            title=ft.Text(
                "Helping Players Enjoy D&D", style=page.theme.text_theme.title_large
            ),
            text=ft.Text(
                "Letting you focus on the game,\nnot the rules.",
                style=page.theme.text_theme.title_medium,
            ),
            logo=ft.Image(
                src=r"/images/logo.png",
                width=67,
                height=28,
                fit=ft.ImageFit.CONTAIN,
            ),
        )

        # update the view data from presenter
        self.race_presenter.update_race_options()

        # register callbacks
        self.race_selection.on_change = on_race_change

        # add style to dropdown
        self.race_selection.text_style = page.theme.text_theme.display_small

        # self.race_presenter.update_name_by_id(race_id=self.race_id)
        # self.race_presenter.update_size_by_id(race_id=self.race_id)
        # self.race_presenter.update_age_by_id(race_id=self.race_id)
        # self.race_presenter.update_weapon_proficiencies_by_id(race_id=self.race_id)

        # Header Row
        header = ft.Column(spacing=0)

        # Add name as a title
        header.controls.append(self.name_control)

        # Add size and age
        header.controls.append(
            ft.Row(
                [
                    ft.Text("Size", style=text_theme.headline_small),
                    self.size_control,
                ]
            )
        )
        header.controls.append(
            ft.Row([ft.Text("Age", style=text_theme.headline_small), self.age_control])
        )

        # Add Weapon Proficiencies
        weapon_proficiencies = ft.Column(spacing=0)
        weapon_proficiencies.controls.append(self.weapon_proficiencies_control)

        content = ft.Column(
            spacing=20,
            controls=[
                hero_section,
                self.race_selection,
                header,
                ft.Divider(thickness=2),
                weapon_proficiencies,
                ft.Divider(thickness=1),
                self.entries_control,
            ],
        )

        race_container = ft.Container(
            content=content,
            height=600,
            alignment=ft.alignment.center,
            margin=0,
            padding=5,
            border_radius=10,
            expand=True,
            # bgcolor=self.background,
        )

        page.add(race_container)
        return

    def set_weapon_proficiencies(self, weapon_proficiencies: list[str]) -> None:
        logger.debug(f"weapon_proficiencies: {weapon_proficiencies}")
        list_dict = {
            "name": "Weapon Proficiencies",
            "items": [
                {"entry_id": i, "entry": {"entry": item}}
                for i, item in enumerate(weapon_proficiencies)
            ],
        }
        logger.debug(f"list_dict: {list_dict}")
        list_container = render_list(list_dict=list_dict)
        self.weapon_proficiencies_control.controls = [list_container]

    def set_name(self, name: str) -> None:
        self.name_control.value = name

    def set_age(self, age: dict[str, int]) -> None:
        age_string = ", ".join(f"{key} - {val}" for key, val in age.items())
        self.age_control.value = age_string

    def set_size(self, size: str) -> None:
        self.size_control.value = size

    def set_race_options(self, options: list[tuple[int, str]]) -> None:
        self.race_selection.options = [
            ft.dropdown.Option(key=key, text=name) for key, name in options
        ]
        # self.race_selection.text_style = ft.TextStyle(font_family="BRLNSB")

    def set_entries(self, entry_set_dict: dict[str, Any]) -> None:
        entries_container = render_entry_set(entry_dict=entry_set_dict)
        self.entries_control.controls = [entries_container]
