import json
import logging
import pathlib
from turtle import back
from typing import Any, Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel, Session
from dnd_player_helper.dnd_model.entry import add_entry_set

from dnd_player_helper.dnd_model.links import (
    ClassSkillLink,
    RaceSkillLink,
    SkillChoiceSkillLink,
)

if TYPE_CHECKING:
    from dnd_player_helper.dnd_model.race import Race
    from dnd_player_helper.dnd_model.dnd_class import DNDClass

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


class Skill(SQLModel, table=True):
    name: str = Field(primary_key=True)
    source: str
    srd: Optional[bool] = Field(default=False)
    basic_rules: Optional[bool] = Field(default=False)
    entry_set_id: Optional[int] = Field(default=None, foreign_key="entryset.id")
    races: Optional[list["Race"]] = Relationship(
        back_populates="skill_proficiencies",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=RaceSkillLink,
    )
    classes: Optional[list["DNDClass"]] = Relationship(
        back_populates="skill_proficiencies",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=ClassSkillLink,
    )
    skill_choices: Optional[list["SkillChoice"]] = Relationship(
        back_populates="skills",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=SkillChoiceSkillLink,
    )


class SkillChoice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    race_id: Optional[int] = Field(foreign_key="race.id")
    dnd_class_name: Optional[int] = Field(foreign_key="dndclass.name")
    count: int
    skills: list[Skill] = Relationship(
        back_populates="skill_choices",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=SkillChoiceSkillLink,
    )
    race: Optional["Race"] = Relationship(
        back_populates="skill_choices", sa_relationship_kwargs={"lazy": "selectin"}
    )
    dnd_class: Optional["DNDClass"] = Relationship(
        back_populates="skill_choices", sa_relationship_kwargs={"lazy": "selectin"}
    )


def add_skill_proficiencies(
    race_dict: dict[str, Any], race: "Race", skills: list["Skill"], session: Session
) -> None:
    skill_proficiencies = race_dict.get("skillProficiencies", None)
    if skill_proficiencies is None:
        return

    logger.info(f"adding skills to race {race.name}")
    logger.info(
        f"Adding skill proficiencies: {skill_proficiencies} to race {race.name}"
    )
    choices_list = []
    race_skills = []
    for skill_proficiency in skill_proficiencies:
        if "any" in skill_proficiency:
            logger.debug(f"Any skill proficiency: {skill_proficiency}")
            skill_count = skill_proficiency["any"]
            choices_list.append(SkillChoice(count=skill_count, skill_choices=skills))
            continue
        if "choose" in skill_proficiency:
            logger.debug(f"Choose skill proficiency: {skill_proficiency}")
            skill_proficiency = skill_proficiency["choose"]
            if "count" in skill_proficiency:
                skill_count = skill_proficiency["count"]
            else:
                skill_count = 1
            skill_choices = [
                get_skill_from_list(skills, skill_name)
                for skill_name in skill_proficiency["from"]
            ]
            choices_list.append(
                SkillChoice(count=skill_count, skill_choices=skill_choices)
            )
            continue
        logger.debug(f"Single skill proficiency: {skill_proficiency}")
        race_skills = [
            get_skill_from_list(skills, skill_name) for skill_name in skill_proficiency
        ]
    if race_skills:
        race.skill_proficiencies = race_skills
    if choices_list:
        race.skill_choices = choices_list
    session.add(race)
    session.commit()


def get_skill_from_list(skill_list: list["Skill"], skill_name: str) -> "Skill":
    for skill in skill_list:
        if skill.name.lower() == skill_name.lower():
            return skill
    raise ValueError(f"Skill {skill_name} not in skill list")


def load_skill(json_file: str) -> dict[str, Any]:
    path = pathlib.Path(json_file)
    with path.open("r") as f:
        json_data = json.load(f)

    return json_data


def get_entries_as_string(entries: list[Any]) -> str:
    text = ""
    for enty in entries:
        if isinstance(enty, str):
            text += enty
        elif isinstance(enty, dict):
            text += get_entries_as_string(enty["items"])
        elif isinstance(enty, list):
            text += get_entries_as_string(enty)
        else:
            logger.error(f"Unknown entry type: {enty}")
    return text


def add_skill(skill_dict: dict[str, Any], session: Session) -> None:
    # get entries
    entries = skill_dict.get("entries", None)
    entry_set_id = None
    if entries:
        try:
            entry_set_id = add_entry_set(entries=entries, session=session)
        except Exception as e:
            logger.error(f"Error adding entry set to skill: {skill_dict.get('name')}")
            raise e

    skill = Skill(
        name=skill_dict["name"],
        source=skill_dict["source"],
        srd=skill_dict.get("srd", False),
        basic_rules=skill_dict.get("basic_rules", False),
        entry_set_id=entry_set_id,
    )
    logger.debug(f"Adding {skill} to the DnD database.")
    session.add(skill)
    session.commit()
