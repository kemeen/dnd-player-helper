import flet as ft
from dnd_player_helper.ui.character_view import CharacterView
from dnd_player_helper.ui.character_details import CharacterDetailView
from dnd_player_helper.ui.navigation import bottom_nav_bar
from dnd_player_helper.ui.router import Router, DataStrategyEnum
from dnd_player_helper.ui.spellbook_view import SpellBookView


def main(page: ft.Page):
    page.title = "DnD Player Helper"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = True

    router = Router(DataStrategyEnum.QUERY)
    router.page = page

    page.on_route_change = router.route_change

    character_view = CharacterView(
        name="Captain Morgan Stormsong",
        class_name="Bard",
        level=2,
        background="Sailor(Pirate)",
        player_name="Kevin",
        race="Half-Elf",
        alignment="Chaotic Good",
        experience_points=1_000_000,
        width=1200,
        height=200,
    )

    character_detail = CharacterDetailView(
        name="Captain Morgan Stormsong",
        age=42,
        character_height="6''",
        weight=180,
        eye_color="Dark Green",
        hair_color="Dark Blond",
        skin_tone="Weathered",
        width=1200,
        height=200,
    )

    spells = {
        1: {
            "slots_total": 3,
            "slots_available": 3,
            "spell_list": [
                "Heroism",
                "Tashas Hideous Laughter",
                "Bane",
                "Cure Wounds",
                "Detect Magic",
            ],
        },
        2: {
            "slots_total": 2,
            "slots_available": 2,
            "spell_list": [
                "Heroism",
                "Tashas Hideous Laughter",
                "Bane",
                "Cure Wounds",
                "Detect Magic",
            ],
        },
        3: {
            "slots_total": 2,
            "slots_available": 2,
            "spell_list": [
                "Heroism",
                "Tashas Hideous Laughter",
                "Bane",
                "Detect Magic",
            ],
        },
        4: {
            "slots_total": 2,
            "slots_available": 2,
            "spell_list": [
                "Heroism",
                "Tashas Hideous Laughter",
                "Detect Magic",
            ],
        },
        5: {
            "slots_total": 2,
            "slots_available": 2,
            "spell_list": [
                "Tashas Hideous Laughter",
            ],
        },
        6: {
            "slots_total": 2,
            "slots_available": 2,
            "spell_list": [
                "Heroism",
                "Detect Magic",
            ],
        },
        7: {
            "slots_total": 2,
            "slots_available": 2,
            "spell_list": [
                "Heroism",
                "Tashas Hideous Laughter",
                "Cure Wounds",
                "Detect Magic",
            ],
        },
        8: {
            "slots_total": 2,
            "slots_available": 2,
            "spell_list": [
                "Heroism",
                "Tashas Hideous Laughter",
            ],
        },
        9: {
            "slots_total": 1,
            "slots_available": 0,
            "spell_list": [
                "Bane",
                "Cure Wounds",
                "Detect Magic",
            ],
        },
    }

    spellbook_view = SpellBookView(
        class_name=["Bard"],
        spellcasting_ability="Charisma",
        spell_save_dc=13,
        spell_attack_bonus=5,
        cantrips=["Vicious Mockery", "Minor Illusion"],
        spells=spells,
        width=1200,
        height=200,
    )

    routes = {
        "/": (character_view, "Character", ft.icons.PERSON),
        "/details": (character_detail, "Details", ft.icons.DETAILS),
        "/spellbook": (spellbook_view, "Spellbook", ft.icons.PODCASTS),
    }

    # navigation bar
    page.navigation_bar = bottom_nav_bar(page=page, routes=routes)

    # add rows to page
    page.add(router.body)
    router.set_routes(routes)

    page.go("/")


ft.app(target=main)
