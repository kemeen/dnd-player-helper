import flet as ft
from .router import Router
from functools import partial


def bottom_nav_bar(routes: dict, page: ft.Page) -> ft.View:
    on_change_func = partial(on_change, routes=[route for route in routes], page=page)

    navigation_bar = ft.CupertinoNavigationBar(
        bgcolor=ft.colors.AMBER_100,
        inactive_color=ft.colors.GREY,
        active_color=ft.colors.BLACK,
        on_change=on_change_func,
        # on_change=lambda e: print("Selected tab:", e.control.selected_index),
        destinations=[
            ft.NavigationDestination(
                icon=icon,
                label=label,
            )
            for route, (view, label, icon) in routes.items()
        ],
    )
    return navigation_bar


def on_change(e: ft.ControlEvent, routes: list, page: ft.Page):
    # print(str(e.__dict__))
    # print(routes[int(e.data)])
    route = routes[int(e.data)]
    print(route)
    page.go(routes[int(e.data)])
