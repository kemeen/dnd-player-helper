import logging
from os import link
from typing import TYPE_CHECKING, Any, Optional
import sqlalchemy
from sqlmodel import Field, Relationship, SQLModel, Session, select, func, or_


from dnd_player_helper.dnd_model.links import (
    # BeastWeaponLink,
    ClassArmorProficiencyLink,
    ClassToolProficiencyLink,
    ClassWeaponProficiencyLink,
    RaceArmorProficiencyLink,
    RaceWeaponProficiencyLink,
    WeaponChoiceWeaponLink,
    WeaponPropertyLink,
    ItemPropertyLink,
)

if TYPE_CHECKING:
    from dnd_player_helper.dnd_model.damage_type import DamageType
    from dnd_player_helper.dnd_model.dnd_class import DNDClass
    from dnd_player_helper.dnd_model.race import Race

    # from dnd_player_helper.dnd_model.beast import Beast

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

# create console handler and set level to debug
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# add formatter to console_handler
console_handler.setFormatter(formatter)

# add console_handler to logger
logger.addHandler(console_handler)


class Item(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    age: Optional[str]
    entry_set_id: Optional[int] = Field(default=None, foreign_key="entryset.id")
    properties: Optional[list["ItemProperty"]] = Relationship(
        back_populates="items",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=ItemPropertyLink,
    )
    rarity: Optional[str]
    type_id: Optional[str] = Field(default=None, foreign_key="itemtype.abbreviation")
    type: Optional["ItemType"] = Relationship(
        back_populates="items", sa_relationship_kwargs={"lazy": "selectin"}
    )
    value: Optional[int]
    weight: Optional[float]
    source: Optional[str]
    srd: bool
    basic_rules: bool
    scf_type: Optional[str]
    classes: Optional[list["DNDClass"]] = Relationship(
        back_populates="tool_proficiencies",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=ClassToolProficiencyLink,
    )


class Weapon(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    weapon_category: str
    basic_rules: bool
    srd: bool
    axe: bool
    bow: bool
    club: bool
    crossbow: bool
    dagger: bool
    firearm: bool
    hammer: bool
    mace: bool
    net: bool
    polearm: bool
    spear: bool
    staff: bool
    sword: bool
    age: Optional[str]
    ammo_type: Optional[str]
    damage: Optional[str]
    weapon_range: Optional[str]
    rarity: Optional[str]
    source: Optional[str]
    reload: Optional[int]
    value: Optional[int]
    weight: Optional[float]
    entry_set_id: Optional[int] = Field(default=None, foreign_key="entryset.id")
    damage_type_name: Optional[str] = Field(default=None, foreign_key="damagetype.name")
    damage_type: Optional["DamageType"] = Relationship(
        back_populates="weapons", sa_relationship_kwargs={"lazy": "selectin"}
    )
    properties: list["ItemProperty"] = Relationship(
        back_populates="weapons",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=WeaponPropertyLink,
    )
    type_id: Optional[str] = Field(default=None, foreign_key="itemtype.abbreviation")
    type: Optional["ItemType"] = Relationship(
        back_populates="weapons", sa_relationship_kwargs={"lazy": "selectin"}
    )
    races: Optional[list["Race"]] = Relationship(
        back_populates="weapon_proficiencies",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=RaceWeaponProficiencyLink,
    )
    classes: Optional[list["DNDClass"]] = Relationship(
        back_populates="weapon_proficiencies",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=ClassWeaponProficiencyLink,
    )
    weapon_choices: Optional[list["WeaponChoice"]] = Relationship(
        back_populates="weapons",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=WeaponChoiceWeaponLink,
    )
    # beasts: Optional[list["Beast"]] = Relationship(
    #     back_populates="weapons",
    #     sa_relationship_kwargs={"lazy": "selectin"},
    #     link_model=BeastWeaponLink,
    # )


class WeaponChoice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    race_id: Optional[int] = Field(default=None, foreign_key="race.id")
    race: Optional[list["Race"]] = Relationship(
        back_populates="weapon_choices", sa_relationship_kwargs={"lazy": "selectin"}
    )
    count: int
    weapons: list[Weapon] = Relationship(
        back_populates="weapon_choices",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=WeaponChoiceWeaponLink,
    )


class Armor(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    source: str
    value: int
    ac: int
    weight: float
    basic_rules: bool
    srd: bool
    stealth: bool
    rarity: Optional[str]
    strength: Optional[int]
    entry_set_id: Optional[int] = Field(default=None, foreign_key="entryset.id")
    type_id: Optional[str] = Field(default=None, foreign_key="itemtype.abbreviation")
    type: Optional["ItemType"] = Relationship(
        back_populates="armors", sa_relationship_kwargs={"lazy": "selectin"}
    )
    races: Optional[list["Race"]] = Relationship(
        back_populates="armor_proficiencies",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=RaceArmorProficiencyLink,
    )
    classes: Optional[list["DNDClass"]] = Relationship(
        back_populates="armor_proficiencies",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=ClassArmorProficiencyLink,
    )
    feats: Optional[list["Feat"]] = Relationship(
        back_populates="armor_proficiencies",
        sa_relationship_kwargs={"lazy": "selectin"}
        link_model=FeatArmorProficiencyLink,


class ItemProperty(SQLModel, table=True):
    abbreviation: str = Field(primary_key=True)
    name: str
    source: Optional[str]
    entry_set_id: Optional[int] = Field(default=None, foreign_key="entryset.id")
    items: list[Item] = Relationship(
        back_populates="properties",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=ItemPropertyLink,
    )
    weapons: list[Weapon] = Relationship(
        back_populates="properties",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=WeaponPropertyLink,
    )


class ItemType(SQLModel, table=True):
    abbreviation: str = Field(primary_key=True)
    name: str
    source: Optional[str]
    entry_set_id: Optional[int] = Field(default=None, foreign_key="entryset.id")
    items: list[Item] = Relationship(
        back_populates="type", sa_relationship_kwargs={"lazy": "selectin"}
    )
    weapons: list[Weapon] = Relationship(
        back_populates="type", sa_relationship_kwargs={"lazy": "selectin"}
    )
    armors: list[Armor] = Relationship(
        back_populates="type", sa_relationship_kwargs={"lazy": "selectin"}
    )


def get_item_type_by_abbreviation(abbreviation: str, session: Session) -> ItemType:
    statement = select(ItemType).where(ItemType.abbreviation == abbreviation)
    result = session.exec(statement)
    try:
        item = result.one()
    except sqlalchemy.exc.NoResultFound as e:
        logger.error(f"Could not find item type with abbreviation {abbreviation}")
        raise e
    return item


def get_item_propetry_by_abbreviation(
    abbreviation: str, session: Session
) -> ItemProperty:
    statement = select(ItemProperty).where(ItemProperty.abbreviation == abbreviation)
    result = session.exec(statement)
    return result.one()


def get_weapon(session: Session, name: str) -> list[Item]:
    statement = select(Item).where(
        Item.weapon == True, func.lower(Item.name) == name.lower()
    )
    result = session.exec(statement)
    return result.one()


def get_weapons_by_category(session: Session, category: str) -> list[Item]:
    statement = select(Item).where(
        Item.weapon == True, func.lower(Item.weapon_category) == category.lower()
    )
    result = session.exec(statement)
    return result.all()


def get_weapons(session: Session, key: str) -> list[Item]:
    statement = select(Weapon).where(
        or_(
            func.lower(Weapon.name) == key.lower(),
            func.lower(Weapon.weapon_category) == key.lower(),
        )
    )
    result = session.exec(statement)
    return result.all()


def get_armor(session: Session, name: str) -> list[Item]:
    statement = select(Item).where(
        Item.armor == True, func.lower(Item.name) == name.lower()
    )
    result = session.exec(statement)
    return result.one()


def add_weapon_proficiency_to_race(
    weapon_proficiencies: dict[str, Any], race: "Race", session: Session
) -> None:
    weapon_choices = []
    weapons = []
    for proficiency_dict in weapon_proficiencies:
        for entry, val in proficiency_dict.items():
            if entry == "choose":
                weapon_choice = choose_weapon_proficiencies(data=val, session=session)
                session.add(weapon_choice)
                weapon_choices.append(weapon_choice)
                continue
            parts = entry.split("|")
            key = parts[0]
            weapons.extend(get_weapons(session=session, key=key))
    race.weapon_choices = weapon_choices
    race.weapon_proficiencies = weapons
    session.add(race)


def choose_weapon_proficiencies(data: dict[str, Any], session: Session) -> WeaponChoice:
    proficiencies = []

    count = data.get("count", 0)
    if count == 0:
        return proficiencies

    from_filter = data.get("fromFilter", None)
    if from_filter is None:
        return proficiencies

    if isinstance(from_filter, str):
        name = from_filter.split("=")[1]
        name = name.split(" ")[0]

        weapons = get_weapons(session=session, key=name)
        return WeaponChoice(count=count, weapons=weapons)

    weapons = []
    for name in from_filter:
        name = name.split("|")[0]
        weapons.extend(get_weapons(session=session, key=name))
    return WeaponChoice(count=count, weapons=weapons)
