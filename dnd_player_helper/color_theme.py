import json
import flet as ft


def import_color_theme(path: str, theme_name=str) -> ft.ColorScheme:
    """Import a color theme from a json file."""
    with open(path, "r") as file:
        data = json.load(file)

    colors = {}
    for color in data["entities"]:
        group = color["tags"][-2]
        if not group == theme_name:
            continue
        color_name = color["tags"][-3].replace("-", "_")
        value = color["value"]

        colors[color_name] = value
    # print(colors)

    return ft.ColorScheme(
        primary=colors.get("primary"),
        primary_container=colors.get("primary_container"),
        secondary=colors.get("secondary"),
        secondary_container=colors.get("secondary_container"),
        background=colors.get("background"),
        surface=colors.get("surface"),
        error=colors.get("error"),
        on_primary=colors.get("on_primary"),
        on_secondary=colors.get("on_secondary"),
        on_background=colors.get("on_background"),
        on_surface=colors.get("on_surface"),
        on_error=colors.get("on_error"),
    )


def import_color_palette(path: str, palette_id: str) -> dict[str, str]:
    """Import a color theme from a json file."""
    with open(path, "r") as file:
        data = json.load(file)

    colors = {}
    for color in data["entities"]:
        group = color["tags"][-2]
        if not color["category_id"] == palette_id:
            continue
        color_name = color["tags"][-2].replace("-", "_")
        value = color["value"]

        colors[color_name] = value
    return colors
