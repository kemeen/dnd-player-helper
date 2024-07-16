import flet as ft


def get_modifier(value: int) -> str:
    modifier = value - 10
    modifier = int(modifier / 2)
    return f"{modifier:+}"


class AttributeView(ft.UserControl):
    def __init__(self, name: str, value: int):
        super().__init__()
        self.name: str = name
        self.value: int = value

    def build(self):
        content = ft.Column(
            [
                ft.Container(
                    ft.Text(
                        self.name,
                        size=12,
                        weight=ft.FontWeight.W_500,
                        color=ft.colors.BLACK,
                    ),
                    width=80,
                    height=20,
                    alignment=ft.alignment.top_center,
                    margin=0,
                    padding=0,
                ),
                ft.Container(
                    ft.Text(
                        get_modifier(self.value),
                        size=32,
                        weight=ft.FontWeight.W_500,
                        color=ft.colors.BLACK,
                    ),
                    width=80,
                    height=50,
                    alignment=ft.alignment.top_center,
                    margin=0,
                    padding=0,
                ),
                ft.Container(
                    ft.Text(
                        str(self.value),
                        size=20,
                        weight=ft.FontWeight.W_500,
                        color=ft.colors.BLACK,
                    ),
                    width=80,
                    height=30,
                    alignment=ft.alignment.center,
                    margin=0,
                    padding=0,
                ),
            ]
        )
        box = ft.Container(
            content=content,
            bgcolor=ft.colors.WHITE,
            margin=0,
            padding=10,
            alignment=ft.alignment.center,
            width=120,
            height=140,
            border_radius=10,
            ink=True,
            # on_click=lambda e: print("Clickable transparent with Ink clicked!"),
            image_src="images/attribute_window.png",
            image_fit=ft.ImageFit.FILL,
        )
        return box
