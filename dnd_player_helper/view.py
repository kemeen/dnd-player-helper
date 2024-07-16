from typing import Protocol
import flet as ft
from dnd_player_helper.color_theme import import_color_palette, import_color_theme
from dnd_player_helper.dnd_model.dnd_class import DNDClass
from dnd_player_helper.dnd_model.race import Race as DNDRace
from dnd_player_helper.dnd_model.race import (
    RaceDescriptions,
    RaceAge,
    RaceWeaponProficiency,
)
from dnd_player_helper.race import Race
from dnd_player_helper.race_view import RaceView
from dnd_player_helper.class_view import ClassView
from dnd_player_helper.theme import text_theme

COLOR_THEME = r"data/theme/material-theme_test/data/tokens.json"


class CharacterPresenter(Protocol):
    def get_character_name(self) -> str:
        ...

    def handle_name_update(self) -> None:
        ...

    def get_character_level(self) -> int:
        ...

    def handle_level_update(self) -> None:
        ...

    def get_character_class(self) -> str:
        ...

    def handle_class_update(self) -> None:
        ...

    def get_race(self) -> str:
        ...

    def handle_race_update(self) -> None:
        ...

    def save_character(self) -> None:
        ...

    def load_character(self) -> None:
        ...

    def get_race_from_list(self, race_name) -> Race:
        ...

    def get_class_from_list(self, class_name) -> DNDClass:
        ...

    def get_list_of_races(self) -> list[str]:
        ...

    def get_list_of_classes(self) -> list[str]:
        ...


class DNDPresenter(Protocol):
    def get_race_ids_and_names(self) -> list[tuple[int, str]]:
        ...

    def get_race_by_id(self, race_id: int) -> DNDRace:
        ...

    def get_race_age_by_id(self, race_id: int) -> list[RaceAge]:
        ...

    def get_race_weapon_proficiencies_by_id(
        self, race_id: int
    ) -> list[RaceWeaponProficiency]:
        ...

    def get_race_descriptions_by_id(self, race_id: int) -> list[RaceDescriptions]:
        ...


class CharacterView:
    def __init__(self) -> None:
        self.character_presenter: CharacterPresenter = None
        self.dnd_presenter: DNDPresenter = None

        self.name = ft.TextField(
            label="Name",
            # text_style=ft.TextThemeStyle.LABEL_MEDIUM,
            # label_style=ft.TextThemeStyle.LABEL_SMALL,
        )
        self.class_name = ft.Dropdown(
            label="Class",
            hint_text="Select a class",
            # text_style=ft.TextThemeStyle.LABEL_MEDIUM,
            # label_style=ft.TextThemeStyle.LABEL_SMALL,
        )
        self.race = ft.Dropdown(
            label="Race",
            hint_text="Select a Race",
            # text_style=ft.TextThemeStyle.LABEL_MEDIUM,
            # label_style=ft.TextThemeStyle.LABEL_SMALL,
        )
        self.level = ft.TextField(
            label="Level",
            input_filter=ft.NumbersOnlyInputFilter(),
            # text_style=ft.TextThemeStyle.LABEL_MEDIUM,
            # label_style=ft.TextThemeStyle.LABEL_SMALL,
        )
        self.character_list = ft.Dropdown(
            label="Characters",
            hint_text="Select a character",
            options=[],
            # text_style=ft.TextThemeStyle.LABEL_MEDIUM,
            # label_style=ft.TextThemeStyle.LABEL_SMALL,
        )
        self.save_character_button = ft.IconButton(icon=ft.icons.SAVE)
        self.details = ft.Container(
            ft.Text("Details", style=ft.TextThemeStyle.BODY_LARGE),
            width=400,
            alignment=ft.alignment.center,
            margin=0,
            padding=0,
        )

        self.dark_mode_switch = ft.Switch(
            label="Dark Mode",
            value=True,
        )

    def create_ui(self, page: ft.Page) -> None:
        def on_name_change(event: ft.ControlEvent) -> None:
            self.character_presenter.handle_name_update(event.control.value)
            page.update()

        def on_class_change(event: ft.ControlEvent) -> None:
            class_name = event.control.value
            self.character_presenter.handle_class_update(event.control.value)
            dnd_class = self.character_presenter.get_class_from_list(
                class_name=class_name
            )
            if dnd_class is None:
                self.details.content = ft.Text(f"No race with name {class_name} found!")
                page.update()
                return
            class_view = ClassView(
                name=dnd_class.name,
                spellcasting_ability=dnd_class.spellcasting_ability,
                hit_die=dnd_class.hit_die,
                saving_throws=dnd_class.saving_throws,
                starting_proficiencies=dnd_class.starting_proficiencies,
                spells_known_progression=dnd_class.spells_known_progression,
                starting_equipment=dnd_class.starting_equipment,
                features=dnd_class.features,
                subclasses=dnd_class.subclasses,
                subclass_features=dnd_class.subclass_features,
            )
            self.details.content = class_view
            page.update()

        def on_race_change(event: ft.ControlEvent) -> None:
            print(event.control)
            print(event.control.value)
            race_id = event.control.value
            # self.character_presenter.handle_race_update(race_name)
            # race = self.character_presenter.get_race_from_list(race_name=race_name)
            # if race is None:
            #     self.details.content = ft.Text(f"No race with name {race_name} found!")
            #     page.update()
            #     return
            race = self.dnd_presenter.get_race_by_id(race_id=race_id)

            # refactor to move this to the presenter so that the view does not need to know about the Race implementation
            race_view = RaceView(
                name=race.name,
                size=race.sizes,
                # speed=race.spe,
                ability_modifier=race.ability_scores,
                # sub_races=[],
                entries=[
                    {
                        "name": desc.name,
                        "entry": desc.entry,
                        "table": desc.table_data,
                        "list": desc.list_data,
                        "inset": desc.inset_data,
                    }
                    for desc in race.descriptions
                ],
                age=[{a.age_type, a.age_in_years} for a in race.ages],
                weapon_proficiencies=[w.weapon for w in race.weapon_proficiencies],
            )
            self.details.content = race_view
            page.update()

        def on_level_change(event: ft.ControlEvent) -> None:
            try:
                value = int(event.control.value)
            except ValueError:
                return
            self.character_presenter.handle_level_update(value)
            page.update()

        def on_window_event(event: ft.ControlEvent) -> None:
            print(event.data)
            if event.data == "close":
                print("closing")
                on_close()

        def on_close() -> None:
            self.save_character(self.get_name())
            page.window_destroy()

        def on_character_select(event: ft.ControlEvent) -> None:
            print(f"Selecting character {event.data}")
            self.character_presenter.load_character(event.data)
            page.update()

        def on_character_save(event: ft.ControlEvent) -> None:
            self.save_character(self.get_name())
            page.update()

        def on_dark_mode_change(event: ft.ControlEvent) -> None:
            if event.control.value:
                page.theme.color_scheme = color_themes["dark"]
                page.theme_mode = "dark"
            else:
                page.theme.color_scheme = color_themes["light"]
                page.theme_mode = "light"
            page.update()

        color_themes = {
            "light": import_color_theme(COLOR_THEME, "light"),
            "dark": import_color_theme(COLOR_THEME, "dark"),
        }
        palette = import_color_palette(COLOR_THEME, "ref.palette")

        page.title = "DnD Player Helper"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.scroll = True
        page.theme = ft.Theme()
        page.theme.text_theme = text_theme
        page.theme.color_scheme = color_themes["dark"]
        page.theme_mode = ft.ThemeMode.DARK

        self.name.value = self.character_presenter.get_character_name()
        self.name.on_change = on_name_change
        self.class_name.value = self.character_presenter.get_character_class()
        self.class_name.on_change = on_class_change
        self.class_name.options = [
            ft.dropdown.Option(name)
            for name in self.character_presenter.get_list_of_classes()
        ]
        self.race.value = self.character_presenter.get_race()
        self.race.on_change = on_race_change
        self.race.options = [
            ft.dropdown.Option(key=key, text=name)
            for key, name in self.dnd_presenter.get_race_ids_and_names()
        ]
        self.level.value = str(self.character_presenter.get_character_level())
        self.level.on_change = on_level_change
        self.character_list.on_change = on_character_select
        self.save_character_button.on_click = on_character_save
        self.dark_mode_switch.on_change = on_dark_mode_change

        content = ft.Row(
            [
                ft.Column(
                    [
                        ft.Row([self.character_list, self.dark_mode_switch]),
                        ft.Divider(),
                        ft.Container(
                            self.name,
                            width=400,
                            height=80,
                            alignment=ft.alignment.top_center,
                            margin=0,
                            padding=0,
                        ),
                        ft.Container(
                            self.class_name,
                            width=400,
                            height=80,
                            alignment=ft.alignment.center,
                            margin=0,
                            padding=0,
                        ),
                        ft.Container(
                            self.race,
                            width=400,
                            height=80,
                            alignment=ft.alignment.center,
                            margin=0,
                            padding=0,
                        ),
                        ft.Container(
                            self.level,
                            width=400,
                            height=80,
                            alignment=ft.alignment.center,
                            margin=0,
                            padding=0,
                        ),
                        self.save_character_button,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                self.details,
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
        )
        page.add(content)
        page.on_window_event = on_window_event
        page.window_prevent_close = True

    def get_name(self) -> str:
        return self.name.value

    def get_class_name(self) -> str:
        return self.class_name.value

    def get_race(self) -> str:
        return self.race.value

    def get_level(self) -> int:
        return int(self.level.value)

    def update_name(self, name: str) -> None:
        self.name.value = name

    def update_class_name(self, class_name: str) -> None:
        self.class_name.value = class_name

    def update_race(self, race: str) -> None:
        self.race.value = race

    def update_level(self, level: int) -> None:
        self.level.value = str(level)

    def update_character_list(self, character_list: list[str]) -> None:
        print("updating character list")
        print(character_list)
        self.character_list.options = [ft.dropdown.Option(c) for c in character_list]

    def load_character(self, character: str) -> None:
        self.character_list.value = character

    def save_character(self, character: str) -> None:
        if character == "":
            return
        print(f"Attempting to save character {character}")
        self.character_presenter.save_character(character)

    def run(self):
        ft.app(target=self.create_ui, view=ft.WEB_BROWSER)
