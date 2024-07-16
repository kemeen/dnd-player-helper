import flet as ft


class Default_Box(ft.UserControl):
    def __init__(self, name: str, content: str, width: int, height: int):
        super().__init__()
        self.name: str = name
        self.content: str = content
        self.width: int = width
        self.height: int = height

    def build(self):
        root_col = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text(self.content, color=ft.colors.BLACK),
                    alignment=ft.alignment.center,
                    padding=10,
                ),
                ft.Container(
                    content=ft.Text(self.name, color=ft.colors.BLACK),
                    alignment=ft.alignment.center,
                    padding=10,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        return ft.Container(
            content=root_col,
            image_src="images/default_box.png",
            image_fit=ft.ImageFit.FILL,
            bgcolor=ft.colors.WHITE,
            width=self.width,
            height=self.height,
        )
