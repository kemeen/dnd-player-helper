"""
['ability', 'additionalSpells', 'armorProficiencies', 'entries', 'expertise', 
'languageProficiencies', 'name', 'optionalfeatureProgression', 'prerequisite', 
'resist', 'savingThrowProficiencies', 'skillProficiencies', 'skillToolLanguageProficiencies', 'source', 
'srd', 'toolProficiencies', 'weaponProficiencies']
"""

import logging
from math import exp
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel
from tomlkit import value
from dnd_player_helper.dnd_model.ability import AttributeChoice, AttributeScore

from dnd_player_helper.dnd_model.item import Armor, Item
from dnd_player_helper.dnd_model.language import LanguageProficiencyOption
from dnd_player_helper.dnd_model.links import FeatArmorProficiencyLink

if TYPE_CHECKING:
    from dnd_player_helper.dnd_model.item import Weapon
    from dnd_player_helper.dnd_model.language import Language, LanguageChoice
    from dnd_player_helper.dnd_model.skill import Skill, SkillChoice
    from dnd_player_helper.dnd_model.spell import Spell

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


class Feat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ability_choices: Optional[list["AttributeChoice"]] = Relationship(
        back_populates="feats", sa_relationship_kwargs={"lazy": "selectin"}
    )
    armor_proficiencies: Optional[list["Armor"]] = Relationship(
        back_populates="feats",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=FeatArmorProficiencyLink,
    )
    enty_set_id: Optional[int] = Field(default=None, foreign_key="entryset.id")
    expertise: Optional["FeatExpertise"] = Field(default=None)
    language_proficiency_option: Optional[list["LanguageProficiencyOption"]] = (
        Relationship(
            back_populates="feats", sa_relationship_kwargs={"lazy": "selectin"}
        )
    )
    name: Optional[str] = Field(default=None)


class FeatExpertise(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)
    value: Optional[int] = Field(default=None)


class FeatPrerequisite(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    races: Optional[list["Race"]] = Relationship(
        back_populates="feats",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=FeatPrerequisiteRaceLink,
    )
    sub_races: Optional[list["SubRace"]] = Relationship(
        back_populates="feats",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=FeatPrerequisiteSubRaceLink,
    )
    spellcasting: Optional[bool] = Field(default=False)
    feats: Optional[list["Feat"]] = Relationship(
        back_populates="feats",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=FeatPrerequisiteFeatLink,
    )
    campaigns: Optional[list["Campaign"]] = Relationship(
        back_populates="feats",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=FeatPrerequisiteCampaignLink,
    )
    backgrounds: Optional[list["Background"]] = Relationship(
        back_populates="feats",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=FeatPrerequisiteBackgroundLink,
    )
    ability_scores: Optional[list["AttributeScore"]] = Relationship(
        back_populates="feats",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=FeatPrerequisiteAttributeScoreLink,
    )
    weapon_proficiencies: Optional[list["Weapon"]] = Relationship(
        back_populates="feats",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=FeatPrerequisiteWeaponLink,
    )
    armor_proficiencies: Optional[list["Armor"]] = Relationship(
        back_populates="feats",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=FeatPrerequisiteArmorLink,
    )
