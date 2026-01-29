import logging
from typing import Any, Protocol
import flet as ft
from dnd_player_helper.ui.entity import render_entry_set
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


class SpellPresenter(Protocol):
    def update_name_by_id(self, race_id: int) -> None:
        ...

    def update_entries_by_spell_id(self, race_id: int) -> None:
        ...

    def update_spell_options(self) -> None:
        ...

    def update_spell_view(self, spell_id: int) -> None:
        ...


class SpellHeader(ft.UserControl):
    def __init__(
        self,
    ):
        super().__init__()
        self.name = ft.Text(style=text_theme.title_medium)
        self.level = ft.Text(style=text_theme.display_small)
        self.school = ft.Text(style=text_theme.display_small)
        self.cast_time = ft.Text(style=text_theme.display_small)
        self.spell_range = ft.Text(style=text_theme.display_small)
        self.spell_components = ft.Text(style=text_theme.display_small)
        self.spell_duration = ft.Text(style=text_theme.display_small)

    def update_spell(
        self,
        name: str,
        level: str,
        school: str,
        cast_time: str,
        spell_range: str,
        spell_components: str,
        spell_duration: str,
    ) -> None:
        self.name.value = name
        self.level.value = level
        self.school.value = f"({school})"
        self.cast_time.value = cast_time
        self.spell_range.value = spell_range
        self.spell_components.value = spell_components
        self.spell_duration.value = spell_duration
        self.update()

    def build(self) -> ft.Container:
        self.content = ft.Column(spacing=0)

        # Add name as a title
        self.content.controls.append(self.name)

        # Add level and school in a row
        self.content.controls.append(
            ft.Row(
                [
                    ft.Text("Level"),
                    self.level,
                    self.school,
                ]
            )
        )

        # Add Casting Time
        self.content.controls.append(ft.Row([ft.Text("Casting Time"), self.cast_time]))

        # Add Range
        self.content.controls.append(ft.Row([ft.Text("Range"), self.spell_range]))

        # Add Components
        self.content.controls.append(
            ft.Row([ft.Text("Components"), self.spell_components])
        )

        # Add Duration
        self.content.controls.append(ft.Row([ft.Text("Duration"), self.spell_duration]))

        return ft.Container(content=self.content)


class SpellView:
    def __init__(self):
        super().__init__()
        self.spell_presenter: SpellPresenter|None = None
        self.spell_selection = ft.Dropdown(
            label="Spell",
            hint_text="Select a Spell",
            width=300,
            dense=True,
        )
        self.entries_control = ft.Column(spacing=0, width=400, scroll=True, height=400)

    def create_ui(self, page: ft.Page) -> None:
        # set theme
        page.fonts = {
            "Brush": "/fonts/BRUSHSCI.ttf",
            "BRLNSB": "/fonts/BRLNSB.ttf",
            "BRLNSDB": "/fonts/BRLNSDB.ttf",
            "BRLNSR": "/fonts/BRLNSR.ttf",
        }
        page.theme = ft.Theme(text_theme=text_theme)

        def on_spell_change(event: ft.ControlEvent) -> None:
            # print(event.control)
            # print(event.control.value)
            spell_id = event.control.value
            # print(spell_id)
            # self.spell_presenter.update_name_by_id(race_id=race_id)
            # self.spell_presenter.update_size_by_id(race_id=race_id)
            # self.spell_presenter.update_age_by_id(race_id=race_id)
            # self.spell_presenter.update_weapon_proficiencies_by_id(race_id=race_id)
            # self.spell_presenter.update_entries_by_race_id(race_id=race_id)
            self.spell_presenter.update_spell_view(spell_id=spell_id)
            self.spell_presenter.update_entries_by_spell_id(spell_id=spell_id)
            # self.header.update_level(level=str(spell_id))
            page.update()

        # initialize spell selection options
        self.spell_presenter.update_spell_options()

        # add style to dropdown
        self.spell_selection.text_style = page.theme.text_theme.display_small

        # add hero section
        self.hero_section = HeroSectionImageRight(
            image=ft.Image(
                src="images/spellcasting_400.png",
                width=400,
                # height=441,
                fit=ft.ImageFit.NONE,
                repeat=ft.ImageRepeat.NO_REPEAT,
            ),
            title=ft.Text("Spellcasting", style=page.theme.text_theme.title_large),
            text=ft.Text(
                "",
                style=page.theme.text_theme.title_medium,
            ),
            logo=ft.Image(
                src=r"/images/logo.png",
                width=67,
                height=28,
                fit=ft.ImageFit.CONTAIN,
            ),
            call_to_action=self.spell_selection,
        )

        self.header = SpellHeader()

        # # update the view data from presenter
        # self.spell_presenter.update_race_options()

        # register callbacks
        self.spell_selection.on_change = on_spell_change

        # # Add name as a title
        # header.controls.append(self.name_control)

        # # Add size and age
        # header.controls.append(
        #     ft.Row(
        #         [
        #             ft.Text("Size", style=text_theme.headline_small),
        #             self.size_control,
        #         ]
        #     )
        # )
        # header.controls.append(
        #     ft.Row([ft.Text("Age", style=text_theme.headline_small), self.age_control])
        # )

        # # Add Weapon Proficiencies
        # weapon_proficiencies = ft.Column(spacing=0)
        # weapon_proficiencies.controls.append(self.weapon_proficiencies_control)

        content = ft.Column(
            spacing=20,
            controls=[
                self.hero_section,
                self.header,
                ft.Divider(thickness=2),
                self.entries_control,
                # weapon_proficiencies,
                # ft.Divider(thickness=1),
                # self.entries_control,
            ],
        )

        spell_container = ft.Container(
            content=content,
            height=600,
            alignment=ft.alignment.center,
            margin=0,
            padding=5,
            border_radius=10,
            expand=True,
            # bgcolor=self.background,
        )

        page.add(spell_container)
        return

    def set_header(
        self,
        level: str,
        name: str,
        school: str,
        cast_time: str,
        spell_range: str,
        spell_components: str,
        spell_duration: str,
    ) -> None:
        logger.debug(f"setting header")
        logger.debug(f"Components: {spell_components}")

        self.header.update_spell(
            level=level,
            name=name,
            school=school,
            cast_time=cast_time,
            spell_range=spell_range,
            spell_components=spell_components,
            spell_duration=spell_duration,
        )

    def set_name(self, name: str) -> None:
        self.name_control.value = name

    def set_age(self, age: dict[str, int]) -> None:
        age_string = ", ".join(f"{key} - {val}" for key, val in age.items())
        self.age_control.value = age_string

    def set_size(self, size: str) -> None:
        self.size_control.value = size

    def set_spell_options(self, options: list[tuple[int, str]]) -> None:
        self.spell_selection.options = [
            ft.dropdown.Option(key=key, text=name) for key, name in options
        ]

    def set_entries(self, entries: list[dict[str, Any]]) -> None:
        # entries_container = render_entry_set(entry_dict=entry_set_dict)
        self.entries_control.controls = [render_entry_set(entries=entries)]
