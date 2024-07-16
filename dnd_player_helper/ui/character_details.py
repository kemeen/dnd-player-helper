import flet as ft
from .default_box import Default_Box
from .attribute_view import AttributeView, get_modifier


class Header(ft.UserControl):
    def __init__(
        self,
        name: str,
        age: int,
        character_height: str,
        weight: int,
        eye_color: str,
        skin_tone: str,
        hair_color: str,
        width: int,
        height: int,
    ):
        super().__init__()
        self.name: str = name
        self.age: int = age
        self.character_height: str = character_height
        self.weight: str = weight
        self.eye_color: str = eye_color
        self.skin_tone: str = skin_tone
        self.hair_color: str = hair_color
        self.width: int = width
        self.height: int = height

    def build(self):
        content_row = ft.Row(spacing=0)
        name_col = ft.Column(
            [
                ft.Container(
                    content=ft.Text(self.name, size=24, color=ft.colors.BLACK),
                    # bgcolor=ft.colors.AMBER_500,
                    width=520,
                    height=self.height,
                    alignment=ft.alignment.Alignment(0.2, 0.15),
                )
            ]
        )
        character_col = ft.Column(width=self.width - 520, height=self.height, spacing=0)
        level_row = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text(
                        str(self.age),
                        size=24,
                        color=ft.colors.BLACK,
                    ),
                    # bgcolor=ft.colors.AMBER_500,
                    width=215,
                    height=int(self.height / 2),
                    alignment=ft.alignment.Alignment(-0.85, 0.9),
                    margin=0,
                    padding=0,
                ),
                ft.Container(
                    content=ft.Text(
                        self.character_height, size=24, color=ft.colors.BLACK
                    ),
                    # bgcolor=ft.colors.AMBER_400,
                    width=215,
                    height=int(self.height / 2),
                    alignment=ft.alignment.Alignment(-0.0, 0.9),
                ),
                ft.Container(
                    content=ft.Text(self.weight, size=24, color=ft.colors.BLACK),
                    # bgcolor=ft.colors.AMBER_400,
                    width=180,
                    height=int(self.height / 2),
                    alignment=ft.alignment.Alignment(-0.7, 0.9),
                ),
            ],
            spacing=0,
        )
        race_row = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text(
                        self.eye_color,
                        size=24,
                        color=ft.colors.BLACK,
                    ),
                    # bgcolor=ft.colors.AMBER_500,
                    width=215,
                    height=int(self.height / 2),
                    alignment=ft.alignment.Alignment(-0.65, -0.3),
                    margin=0,
                    padding=0,
                ),
                ft.Container(
                    content=ft.Text(
                        self.skin_tone,
                        size=24,
                        color=ft.colors.BLACK,
                    ),
                    # bgcolor=ft.colors.AMBER_500,
                    width=215,
                    height=int(self.height / 2),
                    alignment=ft.alignment.Alignment(0.0, -0.3),
                    margin=0,
                    padding=0,
                ),
                ft.Container(
                    content=ft.Text(
                        str(self.hair_color), size=24, color=ft.colors.BLACK
                    ),
                    # bgcolor=ft.colors.AMBER_400,
                    width=180,
                    height=int(self.height / 2),
                    alignment=ft.alignment.Alignment(-0.65, -0.3),
                ),
            ],
            spacing=0,
        )
        character_col.controls.append(level_row)
        character_col.controls.append(race_row)

        content_row.controls.append(name_col)
        content_row.controls.append(character_col)
        header = ft.Container(
            content=content_row,
            # bgcolor=ft.colors.AMBER_500,
            margin=0,
            padding=0,
            alignment=ft.alignment.center,
            width=self.width,
            height=self.height,
            border_radius=10,
            # ink=True,
            # on_click=lambda e: print("Clickable transparent with Ink clicked!"),
            image_src="images/Header.png",
            image_fit=ft.ImageFit.FILL,
        )
        return header


class CharacterDetailView(ft.UserControl):
    def __init__(
        self,
        name: str,
        age: int,
        character_height: str,
        weight: int,
        eye_color: str,
        skin_tone: str,
        hair_color: str,
        width: int,
        height: int,
    ):
        super().__init__()
        self.width: int = width
        self.width: int = height
        self.header: Header = Header(
            name=name,
            age=age,
            character_height=character_height,
            weight=weight,
            eye_color=eye_color,
            skin_tone=skin_tone,
            hair_color=hair_color,
            width=width,
            height=height,
        )

    def build(self):
        character_detail = ft.Column(expand=True)
        # add header row
        header_row = ft.Row(alignment=ft.MainAxisAlignment.START)
        # header_row.controls.append(
        #     ft.Container(bgcolor=ft.colors.AMBER_500, width=1200, height=200)
        # )
        header_row.controls.append(self.header)

        # add main content row
        content_row = ft.Row(alignment=ft.MainAxisAlignment.START, spacing=0)

        # add left column
        left_column = ft.Column(alignment=ft.MainAxisAlignment.START, spacing=0)
        left_column.controls.append(
            Default_Box(
                name="Character Apperance",
                content="Apperance Detail XYZ\n" * 10,
                width=400,
                height=400,
            )
        )
        left_column.controls.append(
            Default_Box(
                name="Character Backstory",
                content="Flavour Text XYZ\n" * 20,
                width=400,
                height=800,
            )
        )

        # add right column
        right_column = ft.Column(alignment=ft.MainAxisAlignment.START, spacing=0)
        right_column.controls.append(
            Default_Box(
                name="Allies & Organizations",
                content="List of Allies and Organizations",
                width=800,
                height=400,
            )
        )
        right_column.controls.append(
            Default_Box(
                name="Additional Features & Traits",
                content="Feature/Trait XYZ\n" * 10,
                width=800,
                height=400,
            )
        )
        right_column.controls.append(
            Default_Box(
                name="Treasure",
                content="Treasure Item XYZ\n" * 10,
                width=800,
                height=400,
            )
        )

        # add columns to content row
        content_row.controls.append(left_column)
        content_row.controls.append(right_column)

        character_detail.controls.append(header_row)
        character_detail.controls.append(content_row)
        return character_detail
