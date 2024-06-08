import json
import logging
import pathlib
from typing import Any, Optional, TYPE_CHECKING
import sqlalchemy

from sqlmodel import Field, SQLModel, Relationship, Session
from dnd_player_helper.dnd_model.entry import add_entry_set
from dnd_player_helper.dnd_model.item import WeaponChoice, get_weapon
from dnd_player_helper.dnd_model.links import (
    RaceArmorProficiencyLink,
    RaceSizeLink,
    RaceSkillLink,
    RaceWeaponProficiencyLink,
)
from dnd_player_helper.dnd_model.size import get_size_by_name

if TYPE_CHECKING:
    from dnd_player_helper.dnd_model.skill import Skill
    from dnd_player_helper.dnd_model.size import Size
    from dnd_player_helper.dnd_model.language import LanguageProficiencyOption
    from dnd_player_helper.dnd_model.height_and_weight import Weight, Height
    from dnd_player_helper.dnd_model.item import Weapon, Armor
    from dnd_player_helper.dnd_model.skill import SkillChoice
    from dnd_player_helper.dnd_model.item import WeaponChoice

logger = logging.getLogger(__name__)

# create console handler and set level to debug
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)

# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# add formatter to console_handler
console_handler.setFormatter(formatter)

# add console_handler to logger
logger.addHandler(console_handler)

ABILITY_SCORE_MAP = {
    "str": "strength",
    "dex": "dexterity",
    "con": "constitution",
    "int": "intelligence",
    "wis": "wisdom",
    "cha": "charisma",
}


class Race(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    source: str
    darkvision: int = Field(default=0)
    srd: Optional[bool] = Field(default=False)
    basic_rules: Optional[bool] = Field(default=False)
    entry_set_id: Optional[int] = Field(default=None, foreign_key="entryset.id")
    ages: list["RaceAge"] = Relationship(
        back_populates="race", sa_relationship_kwargs={"lazy": "selectin"}
    )
    weapon_proficiencies: Optional[list["Weapon"]] = Relationship(
        back_populates="races",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=RaceWeaponProficiencyLink,
    )
    weapon_choices: Optional[list["WeaponChoice"]] = Relationship(
        back_populates="race", sa_relationship_kwargs={"lazy": "selectin"}
    )
    ability_scores: Optional[list["RaceAbilityScore"]] = Relationship(
        back_populates="race", sa_relationship_kwargs={"lazy": "selectin"}
    )
    skill_proficiencies: Optional[list["Skill"]] = Relationship(
        back_populates="races",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=RaceSkillLink,
    )
    skill_choices: Optional[list["SkillChoice"]] = Relationship(
        back_populates="race",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    language_proficiency_options: Optional[
        list["LanguageProficiencyOption"]
    ] = Relationship(
        back_populates="race",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    sizes: Optional[list["Size"]] = Relationship(
        back_populates="races",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=RaceSizeLink,
    )
    weight: Optional["Weight"] = Relationship(
        back_populates="race", sa_relationship_kwargs={"lazy": "selectin"}
    )
    height: Optional["Height"] = Relationship(
        back_populates="race", sa_relationship_kwargs={"lazy": "selectin"}
    )
    armor_proficiencies: Optional[list["Armor"]] = Relationship(
        back_populates="races",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=RaceArmorProficiencyLink,
    )
    # language_options: Optional[list["Language"]] = Relationship(


class RaceAge(SQLModel, table=True):
    race_id: int = Field(primary_key=True, foreign_key="race.id")
    age_type: str = Field(primary_key=True)
    age_in_years: int
    race: Race = Relationship(
        back_populates="ages", sa_relationship_kwargs={"lazy": "selectin"}
    )


class RaceAbilityScore(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    race_id: int = Field(foreign_key="race.id")
    name: str
    abbreviation: str
    value: int
    choices: Optional[list["RaceAbilityScoreChoice"]] = Relationship(
        back_populates="ability_score", sa_relationship_kwargs={"lazy": "selectin"}
    )
    race: Race = Relationship(
        back_populates="ability_scores", sa_relationship_kwargs={"lazy": "selectin"}
    )


class RaceAbilityScoreChoice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ability_score_id: int = Field(foreign_key="raceabilityscore.id")
    abbreviation: str
    name: str
    ability_score: RaceAbilityScore = Relationship(
        back_populates="choices", sa_relationship_kwargs={"lazy": "selectin"}
    )


def get_ability_score_from_race_dict(race_dict: dict[str, Any]) -> list[dict[str, Any]]:
    # check key ability
    scores = race_dict.get("ability", None)
    if scores:
        logger.debug(f'Found key "ability"')
        return scores


def add_race_ability_scores(
    race_dict: dict[str, Any], session: Session, race: Race
) -> None:
    ability_scores = get_ability_score_from_race_dict(race_dict=race_dict)

    name = race_dict.get("name", None)
    source = race_dict.get("source", None)

    if not ability_scores:
        logger.info(f"No abililiy scores found for race {name}-{source}")
        return

    logger.debug(f"{ability_scores}, {type(ability_scores)}, {name}, {source}")

    scores = []
    choices = []

    for ability_score_dict in ability_scores:
        for key, val in ability_score_dict.items():
            if key == "choose":
                ability_score_list = []
                logger.debug(f"Ability Score Choice for {name}-{source}: {key}, {val}")

                if isinstance(val, list):
                    val = {"from": val, "count": 1}

                count = val.get("count", None)
                amount = val.get("amount", None)

                if count:
                    for _ in range(count):
                        score = RaceAbilityScore(
                            name=key,
                            abbreviation=key,
                            value=amount if amount else 1,
                        )
                        scores.append(score)
                    abilities = val.get("from", None)
                elif amount:
                    score = RaceAbilityScore(name=key, abbreviation=key, value=amount)
                    scores.append(score)
                    abilities = val.get("from", None)
                else:
                    raise ValueError(
                        f"Ability score choice {key} for race {race_dict['name']} has no count or amount"
                    )

                for score in ability_score_list:
                    for a in abilities:
                        choices.append(
                            RaceAbilityScoreChoice(
                                abbreviation=a,
                                name=ABILITY_SCORE_MAP[a],
                            )
                        )
                score.choices.extend(choices)
                continue
            if key not in ABILITY_SCORE_MAP:
                raise KeyError(
                    f"Ability score {key} not in {list(ABILITY_SCORE_MAP.keys())}"
                )
            scores.append(
                RaceAbilityScore(
                    name=ABILITY_SCORE_MAP[key],
                    abbreviation=key,
                    value=val,
                )
            )
    race.ability_scores.extend(scores)
    session.add(race)
    session.commit()


def load_race(json_file: str) -> dict[str, Any]:
    path = pathlib.Path(json_file)
    with path.open("r") as f:
        json_data = json.load(f)

    return json_data


def add_race(race_dict: dict[str, Any], session: Session) -> Race:
    # get entries
    entries = race_dict.get("entries", None)
    entry_set_id = None
    if entries:
        try:
            entry_set_id = add_entry_set(entries=entries, session=session)
        except sqlalchemy.exc.ProgrammingError as e:
            logger.error(f"Error adding entry set for race: {race_dict['name']}")
            raise e

    race = Race(
        name=race_dict["name"],
        source=race_dict["source"],
        darkvision=race_dict.get("darkvision", 0),
        srd=race_dict.get("srd", False),
        basic_rules=race_dict.get("basicRules", False),
        entry_set_id=entry_set_id,
    )
    session.add(race)
    return race


def add_race_age(race_dict: dict[str, Any], session: Session, race: Race) -> None:
    age_data = race_dict.get("age", None)
    if age_data is None:
        return
    try:
        for key, val in age_data.items():
            race.ages.append(RaceAge(age_type=key, age_in_years=val))
            session.add(race)
    except ValueError as e:
        logger.error(age_data)
        raise e
    session.commit()


def get_size_from_list(size_list: list["Size"], size_name: str) -> "Size":
    logger.info(f"Size list: {size_list}")
    for size in size_list:
        logger.info(f"Size: {size}")
        if size.name.lower() == size_name.lower():
            return size
    raise ValueError(f"Size {size_name} not in size list")


def add_sizes(
    race_dict: dict[str, any], race: Race, sizes: list["Size"], session: Session
) -> None:
    logger.info(f"Sizes: {str(sizes)}")

    # check if size entry exist
    race_sizes = race_dict.get("size", None)
    if race_sizes is None:
        logger.warning(f"No size entry found for race {race.name}")
        return

    # get sizes for race
    race_sizes_list = [
        get_size_by_name(size_name=size, session=session) for size in race_sizes
    ]

    if race_sizes_list:
        logger.info(f"Adding sizes {race_sizes_list} to race {race.name}, {race.id}")
        race.sizes = race_sizes_list
        session.add(race)
        session.commit()
