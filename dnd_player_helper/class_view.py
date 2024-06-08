from typing import Any
import flet as ft


class ClassView(ft.UserControl):
    def __init__(
        self,
        name: str,
        spellcasting_ability: str = "",
        hit_die: dict[str, int] = {},
        saving_throws: list[str] = [],
        starting_proficiencies: dict[str, Any] = {},
        spells_known_progression: list[int] = [],
        starting_equipment: dict[str, Any] = [],
        features: list[tuple[str, int]] = [],
        subclasses: list[dict[str, Any]] = [],
        subclass_features: dict[str, Any] = {},
        # font_style: dict[str, Any] = {
        #     "title-size": 36,
        #     "title-weight": ft.FontWeight.W_600,
        #     "title-color": ft.colors.BLACK,
        #     "title-font-family": "Old English Text MT",
        #     "h1-size": 16,
        #     "h1-weight": ft.FontWeight.W_500,
        #     "h1-color": ft.colors.BLACK,
        #     "h1-font-family": "RobotoSlab",
        #     "h2-size": 14,
        #     "h2-weight": ft.FontWeight.W_400,
        #     "h2-color": ft.colors.BLACK,
        #     "h2-font-family": "RobotoSlab",
        #     "text-size": 14,
        #     "text-weight": ft.FontWeight.W_300,
        #     "text-color": ft.colors.BLACK,
        #     "text-font-family": "RobotoSlab",
        # },
    ):
        super().__init__()
        self.name: str = name
        self.spellcasting_ability: str = spellcasting_ability
        self.hit_die: dict[str, int] = hit_die
        self.saving_throws: list[str] = saving_throws
        self.starting_proficiencies: dict[str, Any] = starting_proficiencies
        self.spells_known_progression: list[int] = spells_known_progression
        self.starting_equipment: dict[str, Any] = starting_equipment
        self.features: list[tuple[str, int]] = features
        self.subclasses: list[dict[str, Any]] = subclasses
        self.subclass_features: dict[str, Any] = subclass_features
        # self.font_style: dict[str, Any] = font_style

    def build(self):
        # Header Row
        header = ft.Column(
            spacing=0,
            width=800,
        )
        header.controls.append(
            ft.Text(
                self.name,
                style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                # size=self.font_style["title-size"],
                # color=self.font_style["title-color"],
                # weight=self.font_style["title-weight"],
                # font_family=self.font_style["title-font-family"],
            )
        )
        header.controls.append(
            ft.Row(
                [
                    ft.Text(
                        "Spellcasting Ability",
                        style=ft.TextThemeStyle.HEADLINE_SMALL,
                    ),
                    ft.Text(
                        self.spellcasting_ability,
                        style=ft.TextThemeStyle.DISPLAY_MEDIUM,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                width=800,
                spacing=10,
            )
        )
        header.controls.append(
            ft.Row(
                [
                    ft.Text(
                        "Saving Throws",
                        style=ft.TextThemeStyle.DISPLAY_MEDIUM,
                        # size=self.font_style["h1-size"],
                        # color=self.font_style["h1-color"],
                        # weight=self.font_style["h1-weight"],
                        # font_family=self.font_style["h1-font-family"],
                    ),
                    ft.Text(
                        ", ".join(self.saving_throws),
                        # ", ".join([f"{k}: {v} m/turn" for k, v in self.speed.items()]),
                        # size=self.font_style["text-size"],
                        # color=self.font_style["text-color"],
                        # weight=self.font_style["text-weight"],
                        # font_family=self.font_style["text-font-family"],
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                width=800,
                spacing=10,
            )
        )
        header.controls.append(
            ft.Row(
                [
                    ft.Text(
                        "Hit Dice",
                        style=ft.TextThemeStyle.DISPLAY_MEDIUM,
                        # size=self.font_style["h1-size"],
                        # color=self.font_style["h1-color"],
                        # weight=self.font_style["h1-weight"],
                        # font_family=self.font_style["h1-font-family"],
                    ),
                    ft.Text(
                        f'{self.hit_die["number"]}d{self.hit_die["faces"]}',
                        # size=self.font_style["text-size"],
                        # color=self.font_style["text-color"],
                        # weight=self.font_style["text-weight"],
                        # font_family=self.font_style["text-font-family"],
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                width=800,
                spacing=10,
            )
        )

        # Subrace Info Row
        # subrace_info = ft.Column(spacing=0)

        # Proficiencies Row
        proficiencies = ft.Column()
        for group, items in self.starting_proficiencies.items():
            if group in ["toolProficiencies", "skills", "weapons"]:
                continue
            proficiencies.controls.append(
                ft.Column(
                    controls=[
                        ft.Text(
                            group,
                            style=ft.TextThemeStyle.DISPLAY_SMALL,
                            # size=self.font_style["h1-size"],
                            # color=self.font_style["h1-color"],
                            # weight=self.font_style["h1-weight"],
                            # font_family=self.font_style["h1-font-family"],
                        ),
                        ft.Text(
                            ", ".join(items),
                            # size=self.font_style["text-size"],
                            # color=self.font_style["text-color"],
                            # weight=self.font_style["text-weight"],
                            # font_family=self.font_style["text-font-family"],
                            no_wrap=False,
                        ),
                    ],
                    width=800,
                    spacing=0,
                )
            )

        # Features Row
        features = ft.Column()
        # print(self.features)
        features.controls.append(
            ft.Text(
                "Features",
                width=800,
                # size=self.font_style["h1-size"],
                # color=self.font_style["h1-color"],
                # weight=self.font_style["h1-weight"],
                # font_family=self.font_style["h1-font-family"],
            ),
        )
        for feature, level in self.features:
            # if group in ['toolProficiencies']:
            #     continue
            features.controls.append(
                ft.Text(
                    f"{feature} at level {level}",
                    # size=self.font_style["h2-size"],
                    # color=self.font_style["h2-color"],
                    # weight=self.font_style["h2-weight"],
                    # font_family=self.font_style["h2-font-family"],
                    width=800,
                ),
            )

        # Subclasses Row
        subclasses = ft.Column()
        for subclass in self.subclasses:
            # if group in ['toolProficiencies']:
            #     continue
            subclass_features = [f.split("|")[0] for f in subclass["subclassFeatures"]]

            subclasses.controls.append(
                ft.Column(
                    controls=[
                        ft.Text(
                            subclass["name"],
                            width=800,
                            # size=self.font_style["h1-size"],
                            # color=self.font_style["h1-color"],
                            # weight=self.font_style["h1-weight"],
                            # font_family=self.font_style["h1-font-family"],
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "Features",
                                    width=800,
                                    # size=self.font_style["h2-size"],
                                    # color=self.font_style["h2-color"],
                                    # weight=self.font_style["h2-weight"],
                                    # font_family=self.font_style["h2-font-family"],
                                ),
                                ft.Text(
                                    f", ".join(subclass_features),
                                    width=800,
                                    # size=self.font_style["text-size"],
                                    # color=self.font_style["text-color"],
                                    # weight=self.font_style["text-weight"],
                                    # font_family=self.font_style["text-font-family"],
                                    no_wrap=False,
                                ),
                            ],
                            spacing=0,
                        ),
                    ],
                    spacing=0,
                )
            )
        body = ft.Column(
            controls=[
                proficiencies,
                ft.Divider(color=ft.colors.GREY, thickness=1),
                features,
                ft.Divider(color=ft.colors.GREY, thickness=1),
                subclasses,
            ],
            spacing=0,
            scroll=True,
        )
        content = ft.Column(
            spacing=0,
            controls=[
                header,
                ft.Divider(color=ft.colors.BROWN, thickness=2),
                body,
            ],
        )

        return ft.Container(
            theme=ft.Theme(
                color_scheme_seed=ft.colors.BLACK54, text_theme=ft.TextTheme()
            ),
            theme_mode=ft.ThemeMode.LIGHT,
            content=content,
            width=800,
            height=600,
            alignment=ft.alignment.center,
            margin=0,
            padding=5,
            border_radius=10,
            bgcolor=ft.colors.AMBER_200,
            expand=True,
        )
