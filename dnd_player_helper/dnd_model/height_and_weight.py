from email.mime import base
from turtle import back
import flet as ft
import logging
from typing import Any, Optional, TYPE_CHECKING
from dnd_player_helper.dnd_model.dice import Die

from sqlmodel import Field, SQLModel, Relationship, Session

if TYPE_CHECKING:
    from dnd_player_helper.dnd_model.race import Race


class Height(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    race_id: Optional[int] = Field(default=None, foreign_key="race.id")
    base_height: int = Field(default=0)
    height_mod: str = Field(default=None)
    unit: str = Field(default="inches")
    race: Optional["Race"] = Relationship(
        back_populates="height",
        sa_relationship_kwargs={"lazy": "selectin", "uselist": False},
    )

    def roll_height(self) -> int:
        n_dice, die_size = self.height_mod.split("d")
        n_dice = int(n_dice)
        die_size = int(die_size)
        die = Die(die_type=die_size, num_dice=n_dice, modifier=self.base_height)
        return die.roll_dice()


class Weight(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    race_id: Optional[int] = Field(default=None, foreign_key="race.id")
    base_weight: int = Field(default=0)
    weight_mod: str = Field(default=None)
    unit: str = Field(default="pounds")
    race: Optional["Race"] = Relationship(
        back_populates="weight",
        sa_relationship_kwargs={"lazy": "selectin", "uselist": False},
    )


def add_height_to_race(
    race_dict: dict[str, Any], race: "Race", session: Session
) -> None:
    height_dict = race_dict.get("heightAndWeight")
    if height_dict is None:
        return

    base_height = height_dict.get("baseHeight")
    height_mod = height_dict.get("heightMod")
    if any([base_height is None, height_mod is None]):
        return

    height = Height(base_height=base_height, height_mod=height_mod)
    session.add(height)
    race.height = height
    session.add(race)
    session.commit()
    return


def add_weight_to_race(
    race_dict: dict[str, Any], race: "Race", session: Session
) -> None:
    weight_dict = race_dict.get("heightAndWeight")
    if weight_dict is None:
        return

    base_weight = weight_dict.get("baseWeight")
    weight_mod = weight_dict.get("weightMod")
    if any([base_weight is None, weight_mod is None]):
        return

    weight = Weight(base_weight=base_weight, weight_mod=weight_mod)
    session.add(weight)
    race.weight = weight
    session.add(race)
    session.commit()
    return
