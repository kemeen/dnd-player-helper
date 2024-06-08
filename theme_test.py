import pathlib
from turtle import color
from dnd_player_helper.model import Model
from dnd_player_helper.presenter import CharacterPresenter
from dnd_player_helper.view import CharacterView
import flet as ft
from dnd_player_helper.color_theme import import_color_theme, import_color_palette

CHARACTER_FILE = r"morgan.json"
RACES_DATA_PATH = r"C:\software_projects\python\dnd-player-helper\data\race"
CLASSES_DATA_PATH = r"C:\software_projects\python\dnd-player-helper\data\class"
COLOR_THEME = r"data/theme/material-theme_test/data/tokens.json"


def main(page: ft.Page):
    def on_dark_mode_change(event: ft.ControlEvent) -> None:
        if event.control.value:
            page.theme.color_scheme = color_themes["dark"]
            page.theme_mode = "dark"
        else:
            page.theme.color_scheme = color_themes["light"]
            page.theme_mode = "light"
        page.update()

    page.title = "DnD Player Helper"
    page.scroll = True
    page.theme = ft.Theme()
    color_themes = {
        "light": import_color_theme(COLOR_THEME, "light"),
        "dark": import_color_theme(COLOR_THEME, "dark"),
    }
    palette = import_color_palette(COLOR_THEME, "ref.palette")
    print(palette)
    page.theme.color_scheme = color_themes["dark"]
    page.theme_mode = ft.ThemeMode.DARK

    dark_mode_switch = ft.Switch(
        label="Dark Mode",
        value=True,
        on_change=on_dark_mode_change,
    )

    name = ft.TextField(
        label="Name",
    )
    class_name = ft.Dropdown(
        label="Class",
        hint_text="Select a class",
        options=[ft.dropdown.Option("Barbarian"), ft.dropdown.Option("Bard")],
    )
    race = ft.Dropdown(
        label="Race",
        hint_text="Select a Race",
        options=[ft.dropdown.Option("Human"), ft.dropdown.Option("Dwarf")],
    )
    level = ft.TextField(
        label="Level",
        input_filter=ft.NumbersOnlyInputFilter(),
    )
    character_list = ft.Dropdown(
        label="Characters",
        hint_text="Select a character",
        options=[ft.dropdown.Option("Morgan"), ft.dropdown.Option("Loki")],
    )
    save_character_button = ft.IconButton(icon=ft.icons.SAVE)
    details_column_1 = ft.Column(
        [ft.Text("Details 1")],
        # [ft.Text("Details", style=ft.TextThemeStyle.BODY_LARGE)],
        width=200,
        height=200,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    details_column_2 = ft.Column(
        [ft.Text("Details 2")],
        # [ft.Text("Details", style=ft.TextThemeStyle.BODY_LARGE)],
        width=200,
        height=200,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    details_column_3 = ft.Column(
        [ft.Text("Details 3")],
        # [ft.Text("Details", style=ft.TextThemeStyle.BODY_LARGE)],
        width=200,
        height=200,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    details_1 = ft.Container(
        details_column_1,
        alignment=ft.alignment.center,
        bgcolor=ft.colors.PRIMARY_CONTAINER,
    )
    details_2 = ft.Container(
        details_column_2,
        alignment=ft.alignment.center,
        bgcolor=ft.colors.SECONDARY_CONTAINER,
    )
    details_3 = ft.Container(
        details_column_3,
        alignment=ft.alignment.center,
        bgcolor=ft.colors.TERTIARY_CONTAINER,
    )

    primary_containers = [
        get_color_container(color_name, color)
        for color_name, color in palette.items()
        if color_name.startswith("primary")
    ]

    secondary_containers = [
        get_color_container(color_name, color)
        for color_name, color in palette.items()
        if color_name.startswith("secondary")
    ]

    tertiary_containers = [
        get_color_container(color_name, color)
        for color_name, color in palette.items()
        if color_name.startswith("tertiary")
    ]
    error_containers = [
        get_color_container(color_name, color)
        for color_name, color in palette.items()
        if color_name.startswith("error")
    ]
    neutral_containers = [
        get_color_container(color_name, color)
        for color_name, color in palette.items()
        if color_name.startswith("neutral") and not color_name.startswith("neutral_var")
    ]
    neutral_var_containers = [
        get_color_container(color_name, color)
        for color_name, color in palette.items()
        if color_name.startswith("neutral_var")
    ]
    # for color_name, color in primary_colors.items():
    #     print(color_name)
    #     print(color)

    content = ft.Column(
        [
            ft.Row(
                [
                    ft.Column(
                        [
                            character_list,
                            ft.Divider(),
                            name,
                            class_name,
                            race,
                            level,
                            save_character_button,
                            dark_mode_switch,
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Column([details_1, details_2, details_3]),
                ]
            ),
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text("Primary"),
                            ft.Row(primary_containers),
                            ft.Divider(),
                            ft.Text("Secondary"),
                            ft.Row(secondary_containers),
                            ft.Divider(),
                            ft.Text("Tertiary"),
                            ft.Row(tertiary_containers),
                            ft.Divider(),
                            ft.Text("Error"),
                            ft.Row(error_containers),
                            ft.Divider(),
                            ft.Text("Neutral"),
                            ft.Row(neutral_containers),
                            ft.Divider(),
                            ft.Text("Neutral Variant"),
                            ft.Row(neutral_var_containers),
                        ]
                    ),
                ]
            ),
        ]
    )
    page.add(content)


def get_color_container(color_name: str, color: str) -> ft.Container:
    return ft.Container(
        content=ft.Text(color_name),
        width=80,
        height=80,
        padding=2,
        bgcolor=color,
        alignment=ft.alignment.center,
        col={"sm": 6, "md": 2, "xl": 1},
    )


if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER)
