import flet as ft


class Header(ft.UserControl):
    def __init__(
        self,
        class_name: list[str],
        spellcasting_ability: str,
        spell_save_dc: int,
        spell_attack_bonus: int,
        width: int,
        height: int,
    ):
        super().__init__()
        self.class_name: list[str] = class_name
        self.spellcasting_ability: str = spellcasting_ability
        self.spell_save_dc: int = spell_save_dc
        self.spell_attack_bonus: int = spell_attack_bonus
        self.width: int = width
        self.height: int = height

    def build(self):
        controls = [
            ft.Container(
                content=ft.Text(
                    ", ".join(self.class_name), size=24, color=ft.colors.BLACK
                ),
                # bgcolor=ft.colors.AMBER_500,
                width=520,
                height=self.height,
                alignment=ft.alignment.Alignment(0.2, 0.15),
            ),
            ft.Container(
                content=ft.Text(
                    str(self.spellcasting_ability),
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
                content=ft.Text(self.spell_save_dc, size=24, color=ft.colors.BLACK),
                # bgcolor=ft.colors.AMBER_400,
                width=215,
                height=int(self.height / 2),
                alignment=ft.alignment.Alignment(-0.0, 0.9),
            ),
            ft.Container(
                content=ft.Text(
                    self.spell_attack_bonus, size=24, color=ft.colors.BLACK
                ),
                # bgcolor=ft.colors.AMBER_400,
                width=180,
                height=int(self.height / 2),
                alignment=ft.alignment.Alignment(-0.7, 0.9),
            ),
        ]
        content_row = ft.Row(spacing=0, controls=controls)

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


class SpellBookView(ft.UserControl):
    def __init__(
        self,
        class_name: list[str],
        spellcasting_ability: str,
        spell_save_dc: int,
        spell_attack_bonus: int,
        cantrips: list[str],
        spells: dict,
        width: int,
        height: int,
    ):
        super().__init__()
        self.width: int = width
        self.width: int = height
        self.cantrips: list = cantrips
        self.spells: dict = spells
        self.header: Header = Header(
            class_name=class_name,
            spellcasting_ability=spellcasting_ability,
            spell_save_dc=spell_save_dc,
            spell_attack_bonus=spell_attack_bonus,
            width=width,
            height=height,
        )

    def build(self):
        # add header row
        header_row = ft.Row(
            alignment=ft.MainAxisAlignment.START, controls=[self.header]
        )

        # add main content row
        spell_cols = [
            ft.Column(width=400, spacing=0, alignment=ft.MainAxisAlignment.START),
            ft.Column(width=400, spacing=0, alignment=ft.MainAxisAlignment.START),
            ft.Column(width=400, spacing=0, alignment=ft.MainAxisAlignment.START),
        ]

        spell_cols[0].controls.append(
            spell_level_view(
                background_img="./images/Spell_book_header.png",
                spell_level=0,
                slots_total=0,
                slots_available=0,
                spells=self.cantrips,
                width=400,
                height=80,
            )
        )

        for spell_level, spells in self.spells.items():
            spell_col_id = int(spell_level) // 3
            if spell_col_id > 2:
                spell_col_id = 2

            spell_cols[spell_col_id].controls.append(
                spell_level_view(
                    background_img="./images/Spell_book_header.png",
                    spell_level=spell_level,
                    slots_total=spells["slots_total"],
                    slots_available=spells["slots_available"],
                    spells=spells["spell_list"],
                    width=400,
                    height=80,
                )
            )
        content_row = ft.Row(
            alignment=ft.CrossAxisAlignment.START, spacing=0, controls=spell_cols
        )

        spellbook_view = ft.Column(alignment=ft.MainAxisAlignment.START)
        spellbook_view.controls.append(header_row)
        spellbook_view.controls.append(content_row)
        print("SPELLBOOK VIEW BUILD")

        return spellbook_view


# class SpellLevelView(ft.UserControl):
#     def __init__(
#         self,
#         background_img: str,
#         spell_level: int,
#         slots_total: int,
#         slots_available: int,
#         spells: list[str],
#         width: int,
#         height: int,
#     ):
#         super().__init__()
#         self.background_img: str = background_img
#         self.spell_level: int = spell_level
#         self.slots_total: int = slots_total
#         self.slots_available: int = slots_available
#         self.spells: list[str] = spells
#         self._width: int = width
#         self._height: int = height
#         print("SPELLLEVELVIEW CREATED")

#     def build(self):
#         header_row = ft.Column()
#         header_row.controls.append(
#             ft.Container(
#                 content=ft.Text(self.spell_level),
#                 width=50,
#                 alignment=ft.alignment.center,
#             )
#         )
#         header_row.controls.append(
#             ft.Container(content=ft.Text(self.slots_total), width=100)
#         )
#         header_row.controls.append(
#             ft.Container(content=ft.Text(self.slots_available), width=250)
#         )
#         header = ft.Container(
#             image_src=self.background_img,
#             width=self._width,
#             height=self._height,
#             image_fit=ft.ImageFit.FILL,
#             content=header_row,
#         )

#         content_col = ft.Column()
#         content_col.controls.append(ft.Row(header))
#         for spell in self.spells:
#             content_col.controls.append(
#                 ft.Row(spell_checkbox(prepared=False, name=spell))
#             )
#         print("SPELLLEVELVIEW BUILD")
#         spell_level_view = ft.Container(content=content_col)
#         return spell_level_view


def spell_level_view(
    background_img: str,
    spell_level: int,
    slots_total: int,
    slots_available: int,
    spells: list[str],
    width: int,
    height: int,
):
    header_row = ft.Row()
    header_row.controls.append(
        ft.Container(
            content=ft.Text(spell_level, color=ft.colors.BLACK),
            width=40,
            alignment=ft.alignment.center,
        )
    )
    header_row.controls.append(
        ft.Container(content=ft.Text(slots_total, color=ft.colors.BLACK), width=120)
    )
    header_row.controls.append(
        ft.Container(content=ft.Text(slots_available, color=ft.colors.BLACK), width=240)
    )
    header = ft.Container(
        image_src=background_img,
        bgcolor=ft.colors.WHITE,
        width=width,
        height=height,
        image_fit=ft.ImageFit.FILL,
        content=header_row,
    )
    spells_col = ft.Column(width=400, spacing=0)
    for spell in spells:
        spells_col.controls.append(spell_checkbox(prepared=False, name=spell))
    spells_container = ft.Container(
        content=spells_col, bgcolor=ft.colors.WHITE, width=400
    )

    content = ft.Column(controls=[header, spells_container], width=400, spacing=0)

    print("SPELLLEVELVIEW BUILD")
    return content


def spell_checkbox(prepared: bool, name: str) -> ft.View:
    return ft.Checkbox(label=name, adaptive=True, value=prepared)
