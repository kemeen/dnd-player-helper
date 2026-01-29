import flet as ft

def main(page: ft.Page):
    page.title = "D&D Character Sheet"
    page.theme_mode = "light"
    page.padding = 20
    page.scroll = "auto"

    def create_attribute_box(name):
        value_display = ft.Text("0", size=24, text_align=ft.TextAlign.CENTER)
        modifier_display = ft.Text("(0)", size=10, text_align=ft.TextAlign.CENTER)
        
        def update_value(e):
            try:
                value = int(e.control.value)
                value_display.value = str(value)
                modifier = (value - 10) // 2
                modifier_display.value = f"({modifier:+d})"
                page.update()
            except ValueError:
                pass  # Ignore non-integer inputs

        input_field = ft.TextField(
            width=50,
            height=50,
            text_align=ft.TextAlign.CENTER,
            on_change=update_value
        )

        return ft.Container(
            content=ft.Column([
                ft.Text(name.upper(), size=10, text_align=ft.TextAlign.CENTER),
                ft.Stack([
                    input_field,
                    ft.Container(
                        content=value_display,
                        alignment=ft.alignment.center
                    )
                ]),
                modifier_display
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=5,
        )

    def create_skill_checkbox(name, attribute):
        return ft.Container(
            content=ft.Row([
                ft.Checkbox(scale=0.8),
                ft.Text(f"0 {name} ({attribute})", size=12)
            ], spacing=0),
            padding=ft.padding.only(bottom=2)
        )

    # Header
    header = ft.Text("DUNGEONS & DRAGONS", size=24, weight=ft.FontWeight.BOLD)

    # Character Info
    character_info = ft.Column([
        ft.TextField(label="CHARACTER NAME", value="New Adventurer"),
        ft.Row([
            ft.Dropdown(
                label="CLASS",
                options=[
                    ft.dropdown.Option("Choose"),
                    ft.dropdown.Option("Barbarian"),
                    ft.dropdown.Option("Bard"),
                    ft.dropdown.Option("Cleric"),
                    ft.dropdown.Option("Druid"),
                    ft.dropdown.Option("Fighter"),
                    ft.dropdown.Option("Monk"),
                    ft.dropdown.Option("Paladin"),
                    ft.dropdown.Option("Ranger"),
                    ft.dropdown.Option("Rogue"),
                    ft.dropdown.Option("Sorcerer"),
                    ft.dropdown.Option("Warlock"),
                    ft.dropdown.Option("Wizard")
                ],
                width=150
            ),
            ft.TextField(label="SUBCLASS", width=150),
            ft.TextField(label="LEVEL", value="1", width=100),
        ]),
        ft.Row([
            ft.TextField(label="RACE", width=150),
            ft.TextField(label="SUBRACE", width=150),
            ft.TextField(label="CREATURE TYPE", width=150),
        ]),
    ])

    # Attributes
    attributes = ft.Row([
        create_attribute_box("strength"),
        create_attribute_box("dexterity"),
        create_attribute_box("constitution"),
        create_attribute_box("intelligence"),
        create_attribute_box("wisdom"),
        create_attribute_box("charisma"),
    ], wrap=True)

    # Skills
    skills = ft.Column([
        ft.Text("SKILLS", size=14, weight=ft.FontWeight.BOLD),
        create_skill_checkbox("Acrobatics", "Dex"),
        create_skill_checkbox("Animal Handling", "Wis"),
        create_skill_checkbox("Arcana", "Int"),
        create_skill_checkbox("Athletics", "Str"),
        create_skill_checkbox("Deception", "Cha"),
        create_skill_checkbox("History", "Int"),
        create_skill_checkbox("Insight", "Wis"),
        create_skill_checkbox("Intimidation", "Cha"),
        create_skill_checkbox("Investigation", "Int"),
        create_skill_checkbox("Medicine", "Wis"),
        create_skill_checkbox("Nature", "Int"),
        create_skill_checkbox("Perception", "Wis"),
        create_skill_checkbox("Performance", "Cha"),
        create_skill_checkbox("Persuasion", "Cha"),
        create_skill_checkbox("Religion", "Int"),
        create_skill_checkbox("Sleight of Hand", "Dex"),
        create_skill_checkbox("Stealth", "Dex"),
        create_skill_checkbox("Survival", "Wis"),
    ])

    # Main content
    main_content = ft.Column([
        attributes,
        ft.Container(height=10),  # Spacer
        skills
    ])

    # Add all components to the page
    page.add(
        header,
        ft.Container(height=10),  # Spacer
        character_info,
        ft.Container(height=10),  # Spacer
        main_content
    )

ft.app(target=main)