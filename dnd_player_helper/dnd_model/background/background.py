import logging
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from dnd_player_helper.dnd_model.item import Item

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

class Background(SQLModel, table=True):
    # Primary Key
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Attribute Fields
    name: Optional[str] = Field(default=None)
    source: Optional[str] = Field(default=None)
    srd: Optional[bool] = Field(default=None)
    
    # Relations
    additional_spells: Optional[list["Spell"]] = Relationship(back_populates="backgrounds", sa_relationship_kwargs={"lazy": "selectin"})
    class_prerequisites: Optional[list["ClassPrerequisite"]] = Relationship(back_populates="background", sa_relationship_kwargs={"lazy": "selectin"})
    campaign_prerequisites: Optional[list["CampaignPrerequisite"]] = Relationship(back_populates="background", sa_relationship_kwargs={"lazy": "selectin"})
    entry_set_id: Optional[int] = Field(default=None, foreign_key="entryset.id")
    # feats: Optional[str] = Field(default=None)
    language_proficiencies: Optional[list["Language"]] = Relationship(back_populates="backgrounds", sa_relationship_kwargs={"lazy": "selectin"})
    language_proficiency_choice_id: Optional[int] = Field(default=None, foreign_key="languagechoice.id")
    language_proficiency_choice: Optional["LanguageChoice"] = Relationship(back_populates="background", sa_relationship_kwargs={"lazy": "selectin"})
    proficiency_choices: Optional[list["ProficiencyChoice"]] = Relationship(back_populates="background", sa_relationship_kwargs={"lazy": "selectin"})
    skill_proficiencies: Optional["Skill"] = Relationship(back_populates="backgrounds", sa_relationship_kwargs={"lazy": "selectin"})
    skill_proficiency_choice_id: Optional[int] = Field(default=None, foreign_key="skillchoice.id")
    skill_proficiency_choice: Optional["SkillChoice"] = Relationship(back_populates="background", sa_relationship_kwargs={"lazy": "selectin"})
    weapon_proficiencies: Optional[list["Weapon"]] = Relationship(back_populates="backgrounds", sa_relationship_kwargs={"lazy": "selectin"})
    tool_proficiencies: Optional[list["Item"]] = Relationship(back_populates="backgrounds", sa_relationship_kwargs={"lazy": "selectin"})
    tool_proficiency_choices: Optional[list["ItemChoices"]] = Relationship(back_populates="backgrounds", sa_relationship_kwargs={"lazy": "selectin"})
    tool_proficiency_choices_id


