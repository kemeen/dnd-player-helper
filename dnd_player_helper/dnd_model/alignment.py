from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel
from itertools import product

# if TYPE_CHECKING:
#     from dnd_player_helper.dnd_model.beast import Beast

SOCIETY = {"L": "Lawful", "N": "Neutral", "C": "Chaotic"}
MORALIOTIES = {"G": "Good", "N": "Neutral", "E": "Evil"}


class Alignment(SQLModel, table=True):
    short: str = Field(primary_key=True)
    name: str
    description: str
    # beasts: Optional[list["Beast"]] = Relationship(
    #     back_populates="alignment", sa_relationship_kwargs={"lazy": "selectin"}
    # )
    prefix: Optional[str] = Field(default=None)


def get_alignment_short_from_list_of_abbreviations(
    abbreviations: list[str],
) -> list[str]:
    abbreviations = set([a[0] for a in abbreviations])
    society = [a for a in abbreviations if a in SOCIETY]
    moralities = [a for a in abbreviations if a in MORALIOTIES]
    return product(society, moralities)
