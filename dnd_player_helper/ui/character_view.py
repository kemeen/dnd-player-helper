import flet as ft
from .default_box import Default_Box
from .attribute_view import AttributeView, get_modifier


class Header(ft.UserControl):
    def __init__(
        self,
        name: str,
        class_name: str,
        level: int,
        background: str,
        player_name: str,
        race: str,
        alignment: str,
        experience_points: int,
        width: int,
        height: int,
    ):
        super().__init__()
        self.name: str = name
        self.class_name: str = class_name
        self.level: int = level
        self.background: str = background
        self.player_name = player_name
        self.race: str = race
        self.alignment: str = alignment
        self.experience: int = experience_points
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
                        f"{self.class_name} - {self.level}",
                        size=24,
                        color=ft.colors.BLACK,
                    ),
                    # bgcolor=ft.colors.AMBER_500,
                    width=215,
                    height=int(self.height / 2),
                    alignment=ft.alignment.Alignment(-0.65, 0.9),
                    margin=0,
                    padding=0,
                ),
                ft.Container(
                    content=ft.Text(self.background, size=24, color=ft.colors.BLACK),
                    # bgcolor=ft.colors.AMBER_400,
                    width=215,
                    height=int(self.height / 2),
                    alignment=ft.alignment.Alignment(-0.0, 0.9),
                ),
                ft.Container(
                    content=ft.Text(self.player_name, size=24, color=ft.colors.BLACK),
                    # bgcolor=ft.colors.AMBER_400,
                    width=180,
                    height=int(self.height / 2),
                    alignment=ft.alignment.Alignment(-0.65, 0.9),
                ),
            ],
            spacing=0,
        )
        race_row = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text(
                        self.race,
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
                        self.alignment,
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
                        str(self.experience), size=24, color=ft.colors.BLACK
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


class CharacterView(ft.UserControl):
    def __init__(
        self,
        name: str,
        class_name: str,
        level: int,
        background: str,
        player_name: str,
        race: str,
        alignment: str,
        experience_points: int,
        width: int,
        height: int,
    ):
        super().__init__()
        self.width: int = width
        self.width: int = height
        self.header: Header = Header(
            name=name,
            class_name=class_name,
            level=level,
            background=background,
            player_name=player_name,
            race=race,
            alignment=alignment,
            experience_points=experience_points,
            width=width,
            height=height,
        )

    def build(self):
        character_view = ft.Column(expand=True)
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
        left_row = ft.Row(alignment=ft.MainAxisAlignment.START, spacing=0)
        attributes_column = ft.Column(alignment=ft.MainAxisAlignment.START, spacing=0)
        skills_column = ft.Column(alignment=ft.MainAxisAlignment.START, spacing=0)
        for name, value in [
            ("Strength", 12),
            ("Dexterity", 16),
            ("Constitution", 14),
            ("Intelligence", 8),
            ("Wisdom", 10),
            ("Charisma", 16),
        ]:
            attributes_column.controls.append(AttributeView(name=name, value=value))

        skills_column.controls.append(
            Default_Box(name="Inspiration", content="0", width=280, height=100)
        )
        skills_column.controls.append(
            Default_Box(
                name="Proficency Bonus", content=get_modifier(16), width=280, height=100
            )
        )
        skills_column.controls.append(
            Default_Box(
                name="Saving Throws",
                content="Attribute - val\n" * 6,
                width=280,
                height=200,
            )
        )
        skills_column.controls.append(
            Default_Box(
                name="Skills", content="Skill - val\n" * 18, width=280, height=440
            )
        )
        left_row.controls.append(attributes_column)
        left_row.controls.append(skills_column)
        left_column.controls.append(left_row)
        left_column.controls.append(
            Default_Box(
                name="Passive Wisdom(Perception)", content="0", width=400, height=100
            )
        )
        left_column.controls.append(
            Default_Box(
                name="Other Proficiencies & Languages",
                content="Proficiency XYZ - X\n" * 10,
                width=400,
                height=260,
            )
        )

        # add middle column
        middle_column = ft.Column(alignment=ft.MainAxisAlignment.START, spacing=0)
        middle_column.controls.append(
            Default_Box(
                name="AC Block",
                content="AC - Initiative - Speed",
                width=400,
                height=120,
            )
        )
        middle_column.controls.append(
            Default_Box(name="HP Block", content="HP Info", width=400, height=120)
        )
        middle_column.controls.append(
            Default_Box(
                name="Temp HP Block", content="Temp HP Info", width=400, height=120
            )
        )
        middle_column.controls.append(
            Default_Box(
                name="Hit Dice - Death Saves",
                content="Hit Dice - Death Saves",
                width=400,
                height=120,
            )
        )
        middle_column.controls.append(
            Default_Box(
                name="Attacks and Spellcatsing",
                content="Weapon x - atck - DMG\n" * 3,
                width=400,
                height=360,
            )
        )
        middle_column.controls.append(
            Default_Box(
                name="Equipment", content="Equipment XYZ\n" * 6, width=400, height=360
            )
        )

        # add right column
        right_column = ft.Column(alignment=ft.MainAxisAlignment.START, spacing=0)
        right_column.controls.append(
            Default_Box(
                name="Personality Traits", content="Trait Text", width=400, height=120
            )
        )
        right_column.controls.append(
            Default_Box(name="Ideals", content="Ideals Text", width=400, height=120)
        )
        right_column.controls.append(
            Default_Box(name="Bonds", content="Bonds Text", width=400, height=120)
        )
        right_column.controls.append(
            Default_Box(name="Flaws", content="Flaws Text", width=400, height=120)
        )
        right_column.controls.append(
            Default_Box(
                name="Feature and Traits",
                content="Feature XYZ\n" * 12,
                width=400,
                height=720,
            )
        )

        # add columns to content row
        content_row.controls.append(left_column)
        content_row.controls.append(middle_column)
        content_row.controls.append(right_column)

        character_view.controls.append(header_row)
        character_view.controls.append(content_row)
        return character_view
