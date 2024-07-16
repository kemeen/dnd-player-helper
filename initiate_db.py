import json
import logging
import pathlib
from typing import Any
import sqlalchemy

from sqlmodel import Session
from dnd_player_helper.dnd_model.ability import Ability
from dnd_player_helper.dnd_model.condition import Condition
from dnd_player_helper.dnd_model.damage_type import DamageType, get_damage_type_by_name

from dnd_player_helper.dnd_model.dnd_model import DNDModel
from dnd_player_helper.dnd_model.entry import add_entry_set

# from dnd_player_helper.dnd_model.height_and_weight import (
#     add_height_to_race,
#     add_weight_to_race,
# )
from dnd_player_helper.dnd_model.item import (
    Armor,
    Item,
    ItemProperty,
    ItemType,
    Weapon,
    add_weapon_proficiency_to_race,
    get_item_propetry_by_abbreviation,
    get_item_type_by_abbreviation,
)
from dnd_player_helper.dnd_model.language import (
    add_language,
    add_languages,
    load_languages,
)

from dnd_player_helper.dnd_model.race import (
    add_race,
    add_race_ability_scores,
    add_race_age,
    add_sizes,
    load_race,
)
from dnd_player_helper.dnd_model.size import Size
from dnd_player_helper.dnd_model.skill import (
    add_skill,
    load_skill,
    add_skill_proficiencies,
)
from dnd_player_helper.dnd_model.spell import add_spell, add_spell_school


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create console handler and set level to debug
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# add formatter to console_handler
console_handler.setFormatter(formatter)

# add console_handler to logger
logger.addHandler(console_handler)


RACES_DATA_PATH = pathlib.Path(
    r"C:\software_projects\python\dnd-player-helper\data\race"
)
SKILL_DATA_PATH = pathlib.Path(
    r"C:\software_projects\python\dnd-player-helper\data\skill"
)
LANGUAGE_DATA_PATH = pathlib.Path(
    r"C:\software_projects\python\dnd-player-helper\data\language"
)
ALL_LANGUAGES_DATA_PATH = pathlib.Path(
    r"C:\software_projects\python\dnd-player-helper\data\language\all_languages.json"
)
DAMAGE_TYPES_PATH = pathlib.Path(
    r"C:\software_projects\python\dnd-player-helper\data\tables\damage_types.json"
)
ITEM_PROPERTIES_PATH = pathlib.Path(
    r"C:\software_projects\python\dnd-player-helper\data\items\base\itemProperty"
)
ITEM_TYPES_PATH = pathlib.Path(
    r"C:\software_projects\python\dnd-player-helper\data\items\base\itemType"
)
BASE_ITEMS_PATH = pathlib.Path(
    r"C:\software_projects\python\dnd-player-helper\data\items\base\baseitem"
)

SPELLS_PATH = pathlib.Path(r"C:\software_projects\python\dnd-player-helper\data\spell")

BEASTS_PATH = pathlib.Path(
    r"C:\software_projects\python\dnd-player-helper\data\beastiary\beastiary.json"
)
CONDITIONS_PATH = pathlib.Path(
    r"C:\software_projects\python\dnd-player-helper\data\tables\conditions.json"
)
SPELL_SCHOOLS_PATH = pathlib.Path(
    r"C:\software_projects\python\dnd-player-helper\data\tables\spell_schools.json"
)


def add_armor(armor_dict: dict[str, Any], session: Session) -> None:
    armor_type = get_item_type_by_abbreviation(
        abbreviation=armor_dict.get("type"), session=session
    )
    entries = armor_dict.get("entries", [])
    additional_entries = armor_dict.get("additionalEntries", None)
    if additional_entries:
        entries.extend(additional_entries)
    entry_set_id = None
    if entries:
        entry_set_id = add_entry_set(session=session, entries=entries)

    armor = Armor(
        name=armor_dict.get("name", None),
        source=armor_dict.get("source", None),
        value=armor_dict.get("value", None),
        ac=armor_dict.get("ac", None),
        weight=armor_dict.get("weight", None),
        basic_rules=armor_dict.get("basicRules", False),
        srd=armor_dict.get("srd", False),
        stealth=armor_dict.get("stealth", False),
        rarity=armor_dict.get("rarity", None),
        strength=armor_dict.get("strength", None),
        item_type=armor_type,
        entry_set_id=entry_set_id,
    )
    session.add(armor)


def add_weapon(weapon_dict: dict[str, Any], session: Session) -> None:
    damage_type_map = {
        "B": "bludgeoning",
        "P": "piercing",
        "S": "slashing",
        "N": "necrotic",
        "R": "radiant",
    }
    weapon_type = get_item_type_by_abbreviation(
        abbreviation=weapon_dict.get("type"), session=session
    )
    damage_type = weapon_dict.get("dmgType")
    properties = weapon_dict.get("properties", [])

    # get entries
    entries = weapon_dict.get("entries", [])
    additional_entries = weapon_dict.get("additionalEntries", None)
    if additional_entries:
        entries.extend(additional_entries)
    entry_set_id = None
    if entries:
        entry_set_id = add_entry_set(session=session, entries=entries)

    # get damage type
    if damage_type in damage_type_map:
        damage_type = damage_type_map[damage_type]
    if damage_type:
        try:
            damage_type = get_damage_type_by_name(
                damage_type_name=damage_type, session=session
            )
            session.add(damage_type)
        except sqlalchemy.orm.exc.NoResultFound as e:
            logger.error(
                f"Could not find damage type {damage_type} for item {weapon_dict.get('name')}"
            )
            raise e

    # get item properties
    if len(properties) > 0:
        properties = [
            get_item_propetry_by_abbreviation(abbreviation=prop, session=session)
            for prop in properties
        ]

    weapon = Weapon(
        name=weapon_dict.get("name", None),
        weapon_category=weapon_dict.get("weaponCategory", None),
        weapon_range=weapon_dict.get("range", None),
        basic_rules=weapon_dict.get("basicRules", False),
        srd=weapon_dict.get("srd", False),
        axe=weapon_dict.get("axe", False),
        bow=weapon_dict.get("bow", False),
        club=weapon_dict.get("club", False),
        crossbow=weapon_dict.get("crossbow", False),
        dagger=weapon_dict.get("dagger", False),
        firearm=weapon_dict.get("firearm", False),
        hammer=weapon_dict.get("hammer", False),
        mace=weapon_dict.get("mace", False),
        net=weapon_dict.get("net", False),
        polearm=weapon_dict.get("polearm", False),
        spear=weapon_dict.get("spear", False),
        staff=weapon_dict.get("staff", False),
        sword=weapon_dict.get("sword", False),
        age=weapon_dict.get("age", None),
        ammo_type=weapon_dict.get("ammoType", None),
        damage=weapon_dict.get("dmg1", None),
        rarity=weapon_dict.get("rarity", None),
        source=weapon_dict.get("source", None),
        reload=weapon_dict.get("reload", None),
        value=weapon_dict.get("value", None),
        weight=weapon_dict.get("weight", None),
        damage_type=damage_type,
        properties=properties,
        type=weapon_type,
        entry_set_id=entry_set_id,
    )

    session.add(weapon)


def add_item(item_dict: dict[str, Any], session: Session) -> None:
    name = item_dict.get("name", None)
    properties = item_dict.get("properties", [])
    item_type = item_dict.get("type", None)

    # get item type
    if item_type:
        try:
            item_type = get_item_type_by_abbreviation(
                abbreviation=item_type, session=session
            )
        except sqlalchemy.orm.exc.NoResultFound as e:
            logger.error(
                f"Could not find item type with abbreviation {item_type} for item {name}"
            )
            raise e

    # get item properties
    if len(properties) > 0:
        properties = [
            get_item_propetry_by_abbreviation(abbreviation=prop, session=session)
            for prop in properties
        ]

    # get entries
    entries = item_dict.get("entries", [])
    additional_entries = item_dict.get("additionalEntries", None)
    if additional_entries:
        entries.extend(additional_entries)
    entry_set_id = None
    if entries:
        entry_set_id = add_entry_set(session=session, entries=entries)

    item = Item(
        name=item_dict.get("name", None),
        age=item_dict.get("age", None),
        rarity=item_dict.get("rarity", None),
        value=item_dict.get("value", None),
        weight=item_dict.get("weight", None),
        source=item_dict.get("source", None),
        srd=item_dict.get("srd", False),
        basic_rules=item_dict.get("basicRules", False),
        item_type=item_type,
        properties=properties,
        scf_type=item_dict.get("scfType", None),
        entry_set_id=entry_set_id,
    )
    session.add(item)


def add_items(data_path: pathlib.Path, session: Session) -> None:
    for json_file in data_path.glob("*.json"):
        with json_file.open("r") as f:
            json_data = json.load(f)

        # add armor
        if json_data.get("armor", False):
            add_armor(armor_dict=json_data, session=session)
            continue

        # add weapon
        if json_data.get("weapon", False):
            add_weapon(weapon_dict=json_data, session=session)
            continue

        # add item
        add_item(item_dict=json_data, session=session)
    session.commit()


def add_language_table(data_path: pathlib.Path, session: Session) -> None:
    for language_dict in load_languages(json_file=data_path):
        add_language(language_dict=language_dict, session=session)


def add_skill_table(data_path: pathlib.Path, session: Session) -> None:
    for json_file in data_path.glob("*.json"):
        skill_dict = load_skill(json_file=json_file)
        add_skill(skill_dict=skill_dict, session=session)


def add_size_table(session: Session) -> None:
    size_list = [("S", "small"), ("M", "medium"), ("L", "large"), ("V", "variable")]
    for short, long in size_list:
        session.add(Size(name=short, long_name=long))
    session.commit()


def add_damage_types(data_path: pathlib.Path, session: Session) -> None:
    with data_path.open("r") as f:
        json_data = json.load(f)
    source = json_data.get("source", None)
    srd = json_data.get("srd", False)
    basic_rules = json_data.get("basicRules", False)
    for damage_type, description in json_data["rows"]:
        session.add(
            DamageType(
                name=damage_type,
                description=description,
                source=source,
                srd=srd,
                basic_rules=basic_rules,
            )
        )
    session.commit()


def add_item_types(data_path: pathlib.Path, session: Session) -> None:
    for json_file in data_path.glob("*.json"):
        with json_file.open("r") as f:
            json_data = json.load(f)
        source = json_data.get("source", None)
        name = json_data.get("name", None)
        abbreviation = json_data.get("abbreviation", None)

        # check abbreviation TODO move check to Pydantic
        if abbreviation is None:
            raise ValueError(f"No abbreviation found for item type {str(json_file)}")

        # check name TODO move check to Pydantic
        if name is None:
            entries = json_data.get("entries", None)
            name = entries[0].get("name", None)
        if name is None:
            raise ValueError(f"No name found for item type {str(json_file)}")

        # get entries
        entries = json_data.get("entries", None)
        if entries is None:
            entries = json_data.get("entriesTemplate", None)

        entry_set_id = None
        if entries:
            entry_set_id = add_entry_set(session=session, entries=entries)

        # if entries is None:
        #     logger.error(f"Error with {str(json_file)}")
        #     raise ValueError(f"No name found for item property {str(json_file)}")

        session.add(
            ItemType(
                name=name,
                abbreviation=abbreviation,
                source=source,
                entry_set_id=entry_set_id,
            )
        )
    session.commit()


def add_item_properties(data_path: pathlib.Path, session: Session) -> None:
    for json_file in data_path.glob("*.json"):
        with json_file.open("r") as f:
            json_data = json.load(f)
        # get source
        source = json_data.get("source", None)

        # get entries parent
        entries = json_data.get("entries", None)
        if entries is None:
            entries = json_data.get("entriesTemplate", None)

        # get_name
        name = json_data.get("name", None)
        if name is None and entries is None:
            raise ValueError(f"No name found for item property {str(json_file)}")
        try:
            name = entries[0].get("name", None)
        except:
            print(json_data)
            raise ValueError(f"No name found for item property {str(json_file)}")

        # get abbreviation
        abbreviation = json_data.get("abbreviation", None)
        if abbreviation is None:
            raise ValueError(
                f"No abbreviation found for item property {str(json_file)}"
            )

        # get entries
        entry_set_id = None
        if entries:
            entry_set_id = add_entry_set(session=session, entries=entries)

        if entries is None:
            logger.error(f"Error with {str(json_file)}")
            raise ValueError(f"No name found for item property {str(json_file)}")

        item_property = ItemProperty(
            name=name,
            abbreviation=abbreviation,
            source=source,
        )
        if entry_set_id:
            item_property.entry_set_id = entry_set_id
        session.add(item_property)
    session.commit()


def add_abilities(session: Session):
    abilities = {
        "str": "strength",
        "dex": "dexterity",
        "con": "constitution",
        "int": "intelligence",
        "wis": "wisdom",
        "cha": "charisma",
    }
    for name, long_name in abilities.items():
        session.add(Ability(name=name, long_name=long_name))
    session.commit()


def add_race_tables(data_path: pathlib.Path, session: Session, model: DNDModel) -> None:
    race_sizes = model.get_all_sizes(session=session)
    skills = model.get_all_skills(session=session)
    for i, json_file in enumerate(data_path.glob("*.json")):
        race_dict = load_race(json_file=json_file)
        race = add_race(race_dict=race_dict, session=session)
        session.commit()
        session.refresh(race)

        # race size
        add_sizes(
            race_dict=race_dict,
            race=race,
            session=session,
            sizes=race_sizes,
        )
        # session.commit()
        # session.refresh(race)

        # race ages
        add_race_age(race_dict=race_dict, race=race, session=session)

        # race weapon proficiencies
        weapon_proficiencies = race_dict.get("weaponProficiencies", None)
        if weapon_proficiencies:
            logger.debug(race.name)
            logger.debug(weapon_proficiencies)
            add_weapon_proficiency_to_race(
                weapon_proficiencies=weapon_proficiencies, race=race, session=session
            )
            session.commit()

        # # race ability scores
        add_race_ability_scores(race_dict=race_dict, race=race, session=session)

        # # skill proficiencies
        add_skill_proficiencies(
            race_dict=race_dict,
            race=race,
            session=session,
            skills=skills,
        )

        # # Language proficiencies

        language_proficiencies = race_dict.get("languageProficiencies", None)
        if language_proficiencies:
            print(race.name)
            print(language_proficiencies)
            add_languages(race_dict=race_dict, race=race, session=session)

        # # add weight and height
        # add_weight_to_race(race_dict=race_dict, race=race, session=session)
        # add_height_to_race(race_dict=race_dict, race=race, session=session)


def add_spells(data_path: pathlib.Path, session: Session) -> None:
    for spell_dir in data_path.glob("*"):
        if not spell_dir.is_dir():
            continue
        if spell_dir.name != "PHB":
            continue
        logger.debug(spell_dir)

        # iter over all json files in the sub directory
        for json_file in spell_dir.glob("*.json"):
            # open the json and read all keys and print them to the logger
            with json_file.open("r") as f:
                json_data = json.load(f)
            logger.debug(json_data)
            add_spell(spell_dict=json_data, session=session)


# def add_beastiary(data_path: pathlib.Path, session: Session) -> None:
#     # read json file
#     with data_path.open("r") as f:
#         json_data = json.load(f)

#     # iterate over all books as keys and monsters as sub directories
#     monster_keys = set()
#     for book, data in json_data.items():
#         logger.debug(book)
#         for monster in data.get("monster", []):
#             logger.debug(monster.get("name"))

#             # get all keys from the monster and add them to the monster_keys set
#             monster_keys.update(monster.keys())

#     # print all keys from the monster_keys set to the logger, one by one, ordered alphabetically
#     for key in sorted(monster_keys):
#         logger.debug(key)


def add_conditions(data_path: pathlib.Path, session: Session) -> None:
    # read json file
    with data_path.open("r") as f:
        json_data = json.load(f)

    # iterate over all condition types as keys and entries in json_data
    for condition_type, data in json_data.items():
        logger.debug(condition_type)
        for condition in data:
            logger.debug(condition.get("name"))
            entries = condition.get("entries", None)
            entry_set_id = None
            if entries:
                entry_set_id = add_entry_set(session=session, entries=entries)

            condition = Condition(
                name=condition.get("name"),
                type=condition_type,
                source=condition.get("source"),
                srd=condition.get("srd", False),
                basic_rules=condition.get("basicRules", False),
                entry_set_id=entry_set_id,
            )
            session.add(condition)
    session.commit()


def add_spell_schools(data_path: pathlib.Path, session: Session) -> None:
    with data_path.open("r") as f:
        json_data = json.load(f)

    for school in json_data:
        add_spell_school(
            session=session,
            school_short=school.get("short"),
            name=school.get("name"),
            description=school.get("description"),
        )
    session.commit()


def main() -> None:
    model = DNDModel(echo=False)
    model.delete_db()
    model.create_db_and_tables()

    with model.get_session() as session:
        add_abilities(session=session)
        add_damage_types(data_path=DAMAGE_TYPES_PATH, session=session)
        add_item_properties(data_path=ITEM_PROPERTIES_PATH, session=session)
        add_item_types(data_path=ITEM_TYPES_PATH, session=session)
        add_items(data_path=BASE_ITEMS_PATH, session=session)
        add_language_table(data_path=ALL_LANGUAGES_DATA_PATH, session=session)
        add_skill_table(data_path=SKILL_DATA_PATH, session=session)
        add_size_table(session=session)
        add_race_tables(data_path=RACES_DATA_PATH, session=session, model=model)
        add_conditions(data_path=CONDITIONS_PATH, session=session)
        add_spell_schools(data_path=SPELL_SCHOOLS_PATH, session=session)
        add_spells(data_path=SPELLS_PATH, session=session)
        # add_beastiary(data_path=BEASTS_PATH, session=session)


if __name__ == "__main__":
    main()
