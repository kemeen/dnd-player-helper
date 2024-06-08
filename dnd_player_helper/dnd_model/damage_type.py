import logging
from typing import TYPE_CHECKING, Optional
import sqlalchemy
from sqlmodel import Field, Relationship, SQLModel, Session, func, select

from dnd_player_helper.dnd_model.links import (
    SpellDamageImmunityLink,
    SpellDamageInflictsLink,
    SpellDamageResistLink,
    SpellDamageVulnerableLink,
)


if TYPE_CHECKING:
    from dnd_player_helper.dnd_model.item import Weapon
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


class DamageType(SQLModel, table=True):
    name: str = Field(primary_key=True)
    description: str
    source: Optional[str]
    srd: bool
    basic_rules: bool
    weapons: list["Weapon"] = Relationship(
        back_populates="damage_type", sa_relationship_kwargs={"lazy": "selectin"}
    )
    spells_immune: Optional[list["Spell"]] = Relationship(
        back_populates="damage_immunities",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=SpellDamageImmunityLink,
    )
    spells_inflicts: Optional[list["Spell"]] = Relationship(
        back_populates="damage_inflicts",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=SpellDamageInflictsLink,
    )
    spells_resist: Optional[list["Spell"]] = Relationship(
        back_populates="damage_resists",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=SpellDamageResistLink,
    )
    spells_vulnerable: Optional[list["Spell"]] = Relationship(
        back_populates="damage_vulnerabilities",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=SpellDamageVulnerableLink,
    )


def get_damage_type_by_name(damage_type_name: str, session: Session) -> DamageType:
    statement = select(DamageType).where(
        func.lower(DamageType.name) == damage_type_name.lower()
    )
    result = session.exec(statement)
    try:
        damage_type = result.one()
    except sqlalchemy.orm.exc.NoResultFound:
        print(f"Damage type {damage_type_name} not found in database.")
        raise
    return damage_type
