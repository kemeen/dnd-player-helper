import flet as ft
import random

COLORS = [
    ft.colors.RED,
    ft.colors.GREEN,
    ft.colors.BLUE,
    ft.colors.YELLOW,
    ft.colors.AMBER,
    ft.colors.CYAN,
]


def default_container(content: ft.View):
    cont = ft.Container(
        content=content,
        bgcolor=random.choice(COLORS),
    )
    return cont


def main(page: ft.Page):
    page.title = "DnD Player Helper"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    row = ft.ResponsiveRow(
        [
            default_container(ft.Column(col=18, controls=[ft.Text("COL1")])),
            default_container(ft.Column(col=6, controls=[ft.Text("COL2")])),
        ],
        columns=24,
    )
    row_decorator = ft.Container(content=row, bgcolor=ft.colors.AMBER_100)
    col = ft.Column([row_decorator])

    page.add(col)


if __name__ == "__main__":
    ft.app(target=main)
