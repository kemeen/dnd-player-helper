from typing import Any, List, Optional, Union
import flet as ft
from sqlmodel import col


class HeroSectionImageRight(ft.UserControl):
    def __init__(
        self,
        image: ft.Image,
        title: ft.Text,
        text: ft.Text,
        logo: ft.Image,
        call_to_action: Optional[ft.View] = None,
    ):
        super().__init__()
        self._image = image
        self._text = text
        self._logo = logo
        self._title = title
        self._call_to_action = call_to_action

    def build(self) -> ft.Container:
        column = ft.Column(spacing=0)
        logo_row = ft.Row(alignment=ft.MainAxisAlignment.START)
        main_row = ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        # add logo to logo row
        logo_container = ft.Container(content=self._logo)
        logo_row.controls.append(logo_container)

        # add text to main row
        text_column = ft.Column(spacing=10, alignment=ft.MainAxisAlignment.CENTER)
        text_column.controls.append(self._title)
        text_column.controls.append(self._text)
        if self._call_to_action:
            text_column.controls.append(self._call_to_action)
        text_container = ft.Container(content=text_column)
        main_row.controls.append(text_container)

        # add image to main row
        image_container = ft.Container(content=self._image)
        main_row.controls.append(image_container)

        # add rows to content column
        column.controls.append(logo_row)
        column.controls.append(main_row)
        return ft.Container(content=column)
