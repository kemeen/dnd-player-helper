import logging
from turtle import back
from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship

from dnd_player_helper.dnd_model.links import (
    BeastActionTagBeastLink,
    BeastConditionImmunityLink,
    BeastTypeGroupLink,
    BeastWeaponLink,
)

if TYPE_CHECKING:
    from dnd_player_helper.dnd_model.ability import AttributeSet
    from dnd_player_helper.dnd_model.alignment import Alignment
    from dnd_player_helper.dnd_model.item import Weapon
    from dnd_player_helper.dnd_model.condition import Condition


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


"""
['ac', 'action', 'alias', 'alignment', 'attachedItems', 'attribute_set', basicRules', 'conditionImmune', 
'cr', 'damageTags', 'damageTagsLegendary', 'damageTagsSpell', 'dex', 'dragonAge', 'dragonCastingColor', 'environment', 'familiar', 
'group', 'hasFluff', 'hasFluffImages', 'hasToken', 'hp', 'immune', 'int', 'isNamedCreature', 'isNpc', 'languageTags', 'languages', 
'legendary', 'legendaryActions', 'legendaryGroup', 'legendaryHeader', 'level', 'miscTags', 'mythic', 'mythicHeader', 'name', 
'otherSources', 'page', 'passive', 'pbNote', 'reaction', 'reactionHeader', 'reprintedAs', 'resist', 'save', 'savingThrowForced', 
'savingThrowForcedLegendary', 'savingThrowForcedSpell', 'senseTags', 'senses', 'shortName', 'size', 'sizeNote', 'skill', 'soundClip', 
'source', 'speed', 'spellcasting', 'spellcastingTags', 'srd', 'str', 'summonedByClass', 'summonedBySpell', 'summonedBySpellLevel', 
'tokenCredit', 'trait', 'traitTags', 'type', 'variant', 'vulnerable', 'wis']

['aberration', 'beast', 'celestial', 'construct', 'dragon', 'elemental', 'fey', 'fiend', 'giant', 'humanoid', 'monstrosity', 
'ooze', 'plant', 'undead']

"""


class HitPoints(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    average: int = Field(default=None)
    formula: str = Field(default=None)


class BeastEnvironment(SQLModel, table=True):
    name: str = Field(primary_key=True)
    description: Optional[str] = Field(default=None)


class BeastGroup(SQLModel, table=True):
    name: str = Field(primary_key=True)
    description: Optional[str] = Field(default=None)
    beast_types: Optional[list["BeastType"]] = Relationship(
        back_populates="group",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=BeastTypeGroupLink,
    )


class BeastType(SQLModel, table=True):
    name: str = Field(primary_key=True)
    description: Optional[str] = Field(default=None)
    beast_groups: Optional[list["BeastGroup"]] = Relationship(
        back_populates="type",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=BeastTypeGroupLink,
    )


# add class beast as a SQLModel class with the properties ac, actions, alignment, challenge_rating, charisma, condition_immunities, constitution, damage_immunities, damage_resistances, damage_vulnerabilities, dexterity, hit_dice, hit_points, index, intelligence, languages, legendary_actions, name, proficiencies, reactions, senses, size, special_abilities, speed, strength, subtype, type, wisdom, xp
class Beast(SQLModel, table=True):
    """
    ['ac', 'action', 'alias', 'alignment', 'basicRules', 'conditionImmune', 'cr', 'environment','familiar', 'group', 'hp',
    'immune', 'isNamedCreature', 'isNpc', 'languages', 'legendary', 'legendaryGroup', 'legendaryHeader', 'miscTags', 'name', 'otherSources',
    'page', 'passive', 'pbNote', 'reaction', 'reprintedAs', 'resist', 'save', 'savingThrowForced', 'savingThrowForcedLegendary',
    'savingThrowForcedSpell', 'senseTags', 'senses', 'size', 'skill', 'soundClip', 'source', 'speed', 'spellcasting',
    'spellcastingTags', 'srd', 'str', 'summonedBySpell', 'summonedBySpellLevel', 'trait', 'traitTags', 'type', 'variant',
    'vulnerable', 'weapons', 'wis']
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    ac: int = Field(default=None)
    actions: Optional[list["BeastAction"]] = Relationship(
        back_populates="beast", sa_relationship_kwargs={"lazy": "selectin"}
    )
    alias: Optional[list["BeastAlias"]] = Relationship(
        back_populates="beast", sa_relationship_kwargs={"lazy": "selectin"}
    )

    alignment: Optional["Alignment"] = Relationship(
        back_populates="beasts", sa_relationship_kwargs={"lazy": "selectin"}
    )
    attribute_set_id: Optional[int] = Field(default=None, foreign_key="attributeset.id")
    attribute_set: Optional["AttributeSet"] = Relationship(
        back_populates="beasts", sa_relationship_kwargs={"lazy": "selectin"}
    )
    weapons: Optional[list["Weapon"]] = Relationship(
        back_populates="beasts",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=BeastWeaponLink,
    )
    basic_rules: bool = Field(default=False)
    condition_immunities: Optional[list["Condition"]] = Relationship(
        back_populates="beast_immunities",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=BeastConditionImmunityLink,
    )
    challenge_rating: int = Field(default=None)

    damage_immunities: str = Field(default=None)
    damage_resistances: str = Field(default=None)
    damage_vulnerabilities: str = Field(default=None)
    dexterity: str = Field(default=None)
    hit_dice: str = Field(default=None)
    hit_points: str = Field(default=None)
    index: str = Field(default=None)
    intelligence: str = Field(default=None)
    languages: str = Field(default=None)
    legendary_actions: str = Field(default=None)
    name: str = Field(default=None)
    proficiencies: str = Field(default=None)
    reactions: str = Field(default=None)
    senses: str = Field(default=None)
    size: str = Field(default=None)
    special_abilities: str = Field(default=None)
    speed: str = Field(default=None)
    strength: str = Field(default=None)
    subtype: str = Field(default=None)
    type: str = Field(default=None)
    wisdom: str = Field(default=None)
    xp: str = Field(default=None)


class BeastAction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    beast_id: int = Field(default=None, foreign_key="beast.id")
    beast: Optional[Beast] = Relationship(
        back_populates="actions", sa_relationship_kwargs={"lazy": "selectin"}
    )
    name: str = Field(default=None)
    desc: str = Field(default=None)
    attack_bonus: str = Field(default=None)
    damage_dice: str = Field(default=None)
    damage_bonus: str = Field(default=None)
    action_type: str = Field(default=None)
    action_note: Optional[str] = Field(default=None)


class BeastAlias(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    beast_id: int = Field(default=None, foreign_key="beast.id")
    beast: Optional[Beast] = Relationship(
        back_populates="alias", sa_relationship_kwargs={"lazy": "selectin"}
    )
    name: str = Field(default=None)
