import logging
from turtle import back
from typing import TYPE_CHECKING, Optional
from requests import Session
from sqlmodel import Field, Relationship, SQLModel, select, func
from tomlkit import value
from dnd_player_helper.dnd_model import feat

from dnd_player_helper.dnd_model.links import (
    ClassSavingThrowLink,
    SpellAbilityCheckLink,
    SpellSavingThrowLink,
)


if TYPE_CHECKING:
    from dnd_player_helper.dnd_model.dnd_class import DNDClass
    from dnd_player_helper.dnd_model.feat.feat import Feat
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


class Ability(SQLModel, table=True):
    name: str = Field(primary_key=True)
    long_name: str
    classes: Optional[list["DNDClass"]] = Relationship(
        back_populates="saving_throws",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=ClassSavingThrowLink,
    )
    attribute_scores: Optional[list["AttributeScore"]] = Relationship(
        back_populates="ability", sa_relationship_kwargs={"lazy": "selectin"}
    )
    spells: Optional[list["Spell"]] = Relationship(
        back_populates="ability_checks",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=SpellAbilityCheckLink,
    )
    spell_saving_throws: Optional[list["Spell"]] = Relationship(
        back_populates="saving_throws",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=SpellSavingThrowLink,
    )
    spell_choices: Optional[list["Spell"]] = Relationship(
        back_populates="ability_choices",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=SpellAbilityCheckLink,
    )


class AttributeSet(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    attribute_scores: Optional[list["AttributeScore"]] = Relationship(
        back_populates="attribute_set", sa_relationship_kwargs={"lazy": "selectin"}
    )


class AttributeScore(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    ability: "Ability" = Relationship(
        back_populates="attribute_scores", sa_relationship_kwargs={"lazy": "selectin"}
    )
    ability_name: str = Field(default=None, foreign_key="ability.name")
    value: Optional[int] = Field(default=0)
    attribute_set_id: Optional[int] = Field(default=None, foreign_key="attributeset.id")
    attribute_set: Optional["AttributeSet"] = Relationship(
        back_populates="attribute_scores", sa_relationship_kwargs={"lazy": "selectin"}
    )
    attribute_choice_id: Optional[int] = Field(
        default=None, foreign_key="attributechoice.id"
    )
    attribute_choice: Optional["AttributeChoice"] = Relationship(
        back_populates="attribute_scores", sa_relationship_kwargs={"lazy": "selectin"}
    )
    feat_id: Optional[int] = Field(default=None, foreign_key="feat.id")
    feat: Optional["Feat"] = Relationship(
        back_populates="ability_scores", sa_relationship_kwargs={"lazy": "selectin"}
    )


class AttributeChoice(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    attribute_scores: Optional[list["AttributeScore"]] = Relationship(
        back_populates="attribute_choice", sa_relationship_kwargs={"lazy": "selectin"}
    )
    choices: Optional[int] = Field(default=0)
    feat_id: Optional[int] = Field(default=None, foreign_key="feat.id")
    feat: Optional["Feat"] = Relationship(
        back_populates="attribute_scores", sa_relationship_kwargs={"lazy": "selectin"}
    )


def get_ability_by_long_name(session: Session, ability_long_name: str) -> Ability:
    statement = select(Ability).where(
        func.lower(Ability.long_name) == ability_long_name.lower()
    )
    results = session.exec(statement)
    ability = results.one()
    return ability
