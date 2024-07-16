import logging
from typing import TYPE_CHECKING, Optional
from requests import Session
from sqlmodel import Field, Relationship, SQLModel, select, func

from dnd_player_helper.dnd_model.links import (
    # BeastConditionImmunityLink,
    SpellConditionImmunityLink,
    SpellConditionInflictLink,
)

if TYPE_CHECKING:
    from dnd_player_helper.dnd_model.spell import Spell

    # from dnd_player_helper.dnd_model.beast import Beast

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# add formatter to console_handler
console_handler.setFormatter(formatter)

# add console_handler to logger
logger.addHandler(console_handler)


class Condition(SQLModel, table=True):
    name: str = Field(primary_key=True)
    type: str
    source: Optional[str]
    srd: Optional[bool] = Field(default=False)
    basic_rules: Optional[bool] = Field(default=False)
    entry_set_id: Optional[int] = Field(default=None, foreign_key="entryset.id")
    # beast_immunities: Optional[list["Beast"]] = Relationship(
    #     back_populates="condition_immunities",
    #     sa_relationship_kwargs={"lazy": "selectin"},
    #     link_model=BeastConditionImmunityLink,
    # )
    spells_immune: Optional[list["Spell"]] = Relationship(
        back_populates="condition_immunities",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=SpellConditionImmunityLink,
    )
    spells_inflict: Optional[list["Spell"]] = Relationship(
        back_populates="condition_inflicts",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=SpellConditionInflictLink,
    )


def get_condition_by_name(session: Session, name: str) -> Optional[Condition]:
    statement = select(Condition).where(func.lower(Condition.name) == name.lower())
    results = session.exec(statement)
    condition = results.one_or_none()
    if condition is None:
        logger.warning(f"Condition: {name} not found")
    return condition
