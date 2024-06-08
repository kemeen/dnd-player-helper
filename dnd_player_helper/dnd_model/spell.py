import logging
from typing import Any, Optional, TYPE_CHECKING
import sqlalchemy

from sqlmodel import Field, Relationship, SQLModel, Session, func, select
from dnd_player_helper.dnd_model.ability import get_ability_by_long_name
from dnd_player_helper.dnd_model.condition import get_condition_by_name
from dnd_player_helper.dnd_model.damage_type import get_damage_type_by_name
from dnd_player_helper.dnd_model.entry import add_entry_set


from dnd_player_helper.dnd_model.links import (
    SpellAbilityCheckLink,
    SpellAreaTagLink,
    SpellChoiceAbilityLink,
    SpellConditionImmunityLink,
    SpellConditionInflictLink,
    SpellCreatureTypeLink,
    SpellDamageImmunityLink,
    SpellDamageInflictsLink,
    SpellDamageResistLink,
    SpellDamageVulnerableLink,
    SpellDurationEndLink,
    SpellMetaKeyLink,
    SpellMiscTagLink,
    SpellSavingThrowLink,
)

if TYPE_CHECKING:
    from dnd_player_helper.dnd_model.ability import Ability
    from dnd_player_helper.dnd_model.damage_type import DamageType
    from dnd_player_helper.dnd_model.condition import Condition

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

SPELL_AREA_TAGS = {
    "C": "Cube",
    "E": "Eye",
    "H": "Hemisphere",
    "L": "Line",
    "MT": "Multiple Targets",
    "N": "Cone",
    "P": "Point",
    "Q": "Square",
    "R": "Radius",
    "S": "Sphere",
    "ST": "Single Target",
    "T": "Touch",
    "V": "Self",
    "W": "Wall",
    "X": "Special",
    "Y": "Cylinder",
}


class Spell(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ability_checks: Optional[list["Ability"]] = Relationship(
        back_populates="spells",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=SpellAbilityCheckLink,
    )
    area_tags: Optional[list["AreaTag"]] = Relationship(
        back_populates="spells",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=SpellAreaTagLink,
    )
    creature_types: Optional[list["CreatureType"]] = Relationship(
        back_populates="spells",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=SpellCreatureTypeLink,
    )
    components: Optional[list["SpellComponent"]] = Relationship(
        back_populates="spell",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    condition_immunities: Optional[list["Condition"]] = Relationship(
        back_populates="spells_immune",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=SpellConditionImmunityLink,
    )
    condition_inflicts: Optional[list["Condition"]] = Relationship(
        back_populates="spells_inflict",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=SpellConditionInflictLink,
    )
    damage_immunities: Optional[list["DamageType"]] = Relationship(
        back_populates="spells_immune",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=SpellDamageImmunityLink,
    )
    damage_inflicts: Optional[list["DamageType"]] = Relationship(
        back_populates="spells_inflicts",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=SpellDamageInflictsLink,
    )
    damage_resists: Optional[list["DamageType"]] = Relationship(
        back_populates="spells_resist",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=SpellDamageResistLink,
    )
    damage_vulnerabilities: Optional[list["DamageType"]] = Relationship(
        back_populates="spells_vulnerable",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=SpellDamageVulnerableLink,
    )
    durations: Optional[list["SpellDuration"]] = Relationship(
        back_populates="spell",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    entry_set_id: Optional[int] = Field(default=None, foreign_key="entryset.id")
    entries_higher_level_id: Optional[int] = Field(
        default=None, foreign_key="entryset.id"
    )
    level: Optional[int] = Field(default=None)
    meta_keys: Optional[list["SpellMetaKey"]] = Relationship(
        back_populates="spells",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=SpellMetaKeyLink,
    )
    misc_tags: Optional[list["SpellMiscTag"]] = Relationship(
        back_populates="spells",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=SpellMiscTagLink,
    )
    name: Optional[str] = Field(default=None)
    range_id: Optional[int] = Field(default=None, foreign_key="spellrange.id")
    range: Optional["SpellRange"] = Relationship(
        back_populates="spell",
        sa_relationship_kwargs={
            "lazy": "selectin",
        },
    )
    saving_throws: Optional[list["Ability"]] = Relationship(
        back_populates="spell_saving_throws",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=SpellSavingThrowLink,
    )
    scaling_id: Optional[int] = Field(default=None, foreign_key="spellscaling.id")
    scaling: Optional["SpellScaling"] = Relationship(
        back_populates="spell",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    school_id: Optional[str] = Field(default=None, foreign_key="spellschool.short")
    school: Optional["SpellSchool"] = Relationship(
        back_populates="spells",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    source: Optional[str] = Field(default=None)
    srd: Optional[bool] = Field(default=False)
    basic_rules: Optional[bool] = Field(default=False)
    spell_cast_times: Optional[list["SpellCastTime"]] = Relationship(
        back_populates="spell", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def to_dict(self):
        logger.debug(f"Converting spell {self.name} to dict")
        logger.debug(f"Spell {self.name} has {len(self.spell_cast_times)} cast times")
        logger.debug(f"Spell {self.name} has {len(self.components)} components")
        return {
            # "ability_checks": [ability_check.to_dict() for ability_check in self.ability_checks],
            # "area_tags": [area_tag.to_dict() for area_tag in self.area_tags],
            # "creature_types": [creature_type.to_dict() for creature_type in self.creature_types],
            "components": [component.to_str() for component in self.components],
            # "condition_immunities": [condition_immunity.to_dict() for condition_immunity in self.condition_immunities],
            # "condition_inflicts": [condition_inflict.to_dict() for condition_inflict in self.condition_inflicts],
            # "damage_immunities": [damage_immunity.to_dict() for damage_immunity in self.damage_immunities],
            # "damage_inflicts": [damage_inflict.to_dict() for damage_inflict in self.damage_inflicts],
            # "damage_resists": [damage_resist.to_dict() for damage_resist in self.damage_resists],
            # "damage_vulnerabilities": [damage_vulnerability.to_dict() for damage_vulnerability in self.damage_vulnerabilities],
            "durations": [duration.to_str() for duration in self.durations],
            "entry_set_id": self.entry_set_id,
            "entries_higher_level_id": self.entries_higher_level_id,
            "level": self.level,
            # "meta_keys": [meta_key.to_dict() for meta_key in self.meta_keys],
            # "misc_tags": [misc_tag.to_dict() for misc_tag in self.misc_tags],
            "name": self.name,
            "spell_range": self.range.to_str() if self.range else None,
            # "saving_throws": [saving_throw.to_dict() for saving_throw in self.saving_throws],
            # "scaling_id": self.scaling_id,
            # "scaling": self.scaling.to_dict(),
            # "school_id": self.school_id,
            "school": self.school.name if self.school else None,
            "source": self.source,
            "srd": self.srd,
            "basic_rules": self.basic_rules,
            "spell_cast_times": [
                spell_cast_time.to_str() for spell_cast_time in self.spell_cast_times
            ],
        }


class AreaTag(SQLModel, table=True):
    short: str = Field(primary_key=True)
    name: str
    spells: Optional[list["Spell"]] = Relationship(
        back_populates="area_tags",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=SpellAreaTagLink,
    )


class SpellSchool(SQLModel, table=True):
    short: str = Field(primary_key=True)
    name: str = Field(default=None)
    description: Optional[str] = Field(default=None)
    spells: Optional[list["Spell"]] = Relationship(
        back_populates="school",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class SpellDuration(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    value: Optional[int] = Field(default=None)
    unit: Optional[str] = Field(default=None)
    duration_type: Optional[str] = Field(default=None)
    concentration: bool = Field(default=False)
    up_to: bool = Field(default=False)
    ends: Optional[list["SpellDurationEnd"]] = Relationship(
        back_populates="spell_duration",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    spell_id: Optional[int] = Field(default=None, foreign_key="spell.id")
    spell: Optional["Spell"] = Relationship(
        back_populates="durations",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    def to_str(self):
        if self.duration_type == "instant":
            return f"{self.duration_type}"

        if self.duration_type == "permanent":
            return f"Ends with {', '.join([end.name for end in self.ends])}"

        if self.duration_type == "timed":
            if self.up_to:
                return_str = f"Up to {self.value} {self.unit}"
            else:
                return_str = f"{self.value} {self.unit}"
            if self.concentration:
                return_str += " (concentration)"
            return f"Up to {self.value} {self.unit}"

        if self.duration_type == "special":
            return f"{self.duration_type}"
        logger.error(f"Unknown duration type: {self.duration_type}")
        raise ValueError(f"Unknown duration type: {self.duration_type}")


class SpellDurationEnd(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    spell_duration_id: Optional[int] = Field(
        default=None, foreign_key="spellduration.id"
    )
    spell_duration: Optional["SpellDuration"] = Relationship(
        back_populates="ends",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class SpellComponent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    short: str
    description: Optional[str] = Field(default=None)
    spell_id: Optional[int] = Field(default=None, foreign_key="spell.id")
    spell: Optional["Spell"] = Relationship(
        back_populates="components",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    def to_str(self):
        if self.description:
            return f"{self.short} ({self.description})"
        return self.short


class CreatureType(SQLModel, table=True):
    name: str = Field(primary_key=True)
    spells: Optional[list["Spell"]] = Relationship(
        back_populates="creature_types",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=SpellCreatureTypeLink,
    )


class SpellMetaKey(SQLModel, table=True):
    key: str = Field(primary_key=True)
    spells: Optional[list["Spell"]] = Relationship(
        back_populates="meta_keys",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=SpellMetaKeyLink,
    )


class SpellMiscTag(SQLModel, table=True):
    name: str = Field(primary_key=True)
    spells: Optional[list["Spell"]] = Relationship(
        back_populates="misc_tags",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=SpellMiscTagLink,
    )


class SpellRange(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    value: Optional[int] = Field(default=None)
    unit: Optional[str] = Field(default=None)
    range_type: Optional[str] = Field(default=None)
    spell_id: Optional[int] = Field(default=None)
    spell: Optional["Spell"] = Relationship(
        back_populates="range",
        sa_relationship_kwargs={"lazy": "selectin", "uselist": False},
    )

    def to_dict(self):
        return {
            "value": self.value,
            "unit": self.unit,
            "range_type": self.range_type,
        }

    def to_str(self):
        return f"{self.value} {self.unit} ({self.range_type})"


class SpellScaling(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    label: Optional[str] = Field(default=None)
    spell_id: Optional[int] = Field(default=None)
    spell: Optional["Spell"] = Relationship(
        back_populates="scaling",
        sa_relationship_kwargs={"lazy": "selectin", "uselist": False},
    )
    scale_levels: Optional[list["SpellScaleLevel"]] = Relationship(
        back_populates="spell_scaling",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class SpellScaleLevel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    level: Optional[int] = Field(default=None)
    dice_string: Optional[str] = Field(default=None)
    spell_scaling_id: Optional[int] = Field(default=None, foreign_key="spellscaling.id")
    spell_scaling: Optional["SpellScaling"] = Relationship(
        back_populates="scale_levels",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class SpellCastTime(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    value: Optional[int] = Field(default=None)
    unit: Optional[str] = Field(default=None)
    condition: Optional[str] = Field(default=None)
    spell_id: Optional[int] = Field(default=None, foreign_key="spell.id")
    spell: Optional["Spell"] = Relationship(
        back_populates="spell_cast_times",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    def to_str(self):
        if self.condition:
            return f"{self.value} {self.unit} ({self.condition})"
        else:
            return f"{self.value} {self.unit}"


class SpellChoice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    spells: Optional[list["Spell"]] = Relationship(
        back_populates="choices",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    abilities: Optional[list["Ability"]] = Relationship(
        back_populates="spell_choices",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=SpellChoiceAbilityLink,
    )


def add_spell(session: Session, spell_dict: dict) -> None:
    # check for basic rules
    spell_basic_rules = spell_dict.get("basicRules", False)

    # check for name
    spell_name = spell_dict.get("name")

    # check for level
    spell_level = spell_dict.get("level")

    # check for source
    spell_source = spell_dict.get("source")

    # check for srd
    srd = spell_dict.get("srd", False)
    if not isinstance(srd, bool):
        srd = True

    # initiate spell
    spell = Spell(
        name=spell_name,
        basic_rules=spell_basic_rules,
        level=spell_level,
        source=spell_source,
        srd=srd,
    )

    logger.debug(f"Adding spell: {spell_name}")
    # session.add(spell)
    # spell = session.refresh(spell)

    # check for ability checks
    # if spell_dict.get("abilityCheck"):
    #     spell.ability_checks = [
    #         get_ability_by_long_name(session=session, ability_long_name=ability_name)
    #         for ability_name in spell_dict["abilityCheck"]
    #     ]

    # check for creature types
    # if spell_dict.get("affectsCreatureType"):
    #     spell.creature_types = [
    #         get_or_add_creature_type(session=session, creature_type_name=creature_type)
    #         for creature_type in spell_dict["affectsCreatureType"]
    #     ]

    # check for area tags
    # if spell_dict.get("areaTags"):
    #     spell.area_tags = [
    #         get_or_add_area_tag(session=session, area_tag_short=area_tag)
    #         for area_tag in spell_dict["areaTags"]
    #     ]

    # check for components
    if spell_dict.get("components"):
        logger.debug(f"Adding components to spell {spell_name}")
        logger.debug(f"components: {spell_dict['components']}")
        spell.components = [
            add_spell_component(
                session=session, spell_component_short=key, spell_component_desc=val
            )
            for key, val in spell_dict["components"].items()
        ]

    # check for condition immunities
    # if spell_dict.get("conditionImmune"):
    #     spell.condition_inflicts = [
    #         get_condition_by_name(session=session, name=condition_name)
    #         for condition_name in spell_dict["conditionImmune"]
    #     ]

    # check for condition inflicts
    # if spell_dict.get("conditionInflict"):
    #     spell.condition_inflicts = [
    #         get_condition_by_name(session=session, name=condition_name)
    #         for condition_name in spell_dict["conditionInflict"]
    #     ]

    # check for damage immunities
    # if spell_dict.get("damageImmune"):
    #     spell.damage_immunities = [
    #         get_damage_type_by_name(session=session, damage_type_name=damage_type)
    #         for damage_type in spell_dict["damageImmune"]
    #     ]

    # check for damage inflicts
    # if spell_dict.get("damageInflict"):
    #     spell.damage_inflicts = [
    #         get_damage_type_by_name(session=session, damage_type_name=damage_type)
    #         for damage_type in spell_dict["damageInflict"]
    #     ]

    # check for damage resists
    # if spell_dict.get("damageResist"):
    #     spell.damage_resists = [
    #         get_damage_type_by_name(session=session, damage_type_name=damage_type)
    #         for damage_type in spell_dict["damageResist"]
    #     ]

    # check for damage vulnerabilities
    # if spell_dict.get("damageVulnerable"):
    #     spell.damage_vulnerabilities = [
    #         get_damage_type_by_name(session=session, damage_type_name=damage_type)
    #         for damage_type in spell_dict["damageVulnerable"]
    #     ]

    # check for duration
    if spell_dict.get("duration"):
        durations = []
        for duration_dict in spell_dict["duration"]:
            duration = duration_dict.get("duration")
            if duration:
                duration_value = duration.get("amount")
                duration_unit = duration.get("type")
                duration_up_to = duration.get("upTo", False)
            else:
                duration_value = None
                duration_unit = None
                duration_up_to = False
            ends = duration_dict.get("ends", [])
            if ends:
                ends = [
                    add_spell_duration_end(session=session, name=duration_end_name)
                    for duration_end_name in duration_dict["ends"]
                ]

            durations.append(
                add_spell_duration(
                    session=session,
                    spell_duration_value=duration_value,
                    spell_duration_unit=duration_unit,
                    duration_type=duration_dict.get("type"),
                    concentration=duration_dict.get("concentration", False),
                    up_to=duration_up_to,
                    ends=ends,
                )
            )
        spell.durations = durations

    # check for entries
    entries = spell_dict.get("entries", None)
    entry_set_id = None
    if entries:
        try:
            entry_set_id = add_entry_set(entries=entries, session=session)
            logger.debug(f"Added entry set for spell: {spell_dict['name']}")
        except sqlalchemy.exc.ProgrammingError as e:
            logger.error(f"Error adding entry set for spell: {spell_dict['name']}")
            raise e
    spell.entry_set_id = entry_set_id

    # check for entries higher level
    entries_high_level = spell_dict.get("entriesHigherLevel", None)
    entry_high_evel_set_id = None
    if entries_high_level:
        try:
            entry_high_evel_set_id = add_entry_set(
                entries=entries_high_level, session=session
            )
        except sqlalchemy.exc.ProgrammingError as e:
            logger.error(f"Error adding entry set for spell: {spell_dict['name']}")
            raise e
    spell.entries_higher_level_id = entry_high_evel_set_id

    # check for meta keys
    # if spell_dict.get("meta"):
    #     spell.meta_keys = [
    #         get_or_add_meta_key(session=session, meta_key=meta_key)
    #         for meta_key in spell_dict["meta"]
    #     ]

    # check for misc tags
    # if spell_dict.get("miscTags"):
    #     spell.misc_tags = [
    #         get_or_add_misc_tag(session=session, misc_tag=misc_tag)
    #         for misc_tag in spell_dict["miscTags"]
    #     ]

    # check for range
    if spell_dict.get("range"):
        logger.debug(f"Adding range to spell {spell_name}")
        distance = spell_dict["range"].get("distance")
        if distance:
            range_value = distance.get("amount")
            range_unit = distance.get("type")
            logger.debug(f"range_value: {range_value}, range_unit: {range_unit}")
        else:
            range_value = None
            range_unit = None
        range_type = spell_dict["range"].get("type")
        spell.range = add_spell_range(
            session=session,
            spell_range_value=range_value,
            spell_range_unit=range_unit,
            range_type=range_type,
        )

    # check for saving throws
    # if spell_dict.get("savingThrow"):
    #     spell.saving_throws = [
    #         get_ability_by_long_name(session=session, ability_long_name=ability_name)
    #         for ability_name in spell_dict["savingThrow"]
    #     ]

    # check for scaling
    # if spell_dict.get("scalingLevelDice"):
    #     spell.scaling = add_spell_scaling(
    #         session=session,
    #         label=spell_dict["scalingLevelDice"].get("label"),
    #         scaling=spell_dict["scalingLevelDice"].get("scaling"),
    #     )

    # check for school
    if spell_dict.get("school"):
        spell.school = get_spell_school(
            session=session, school_short=spell_dict["school"]
        )

    # check for spell cast times
    if spell_dict.get("time"):
        spell_cast_times = [
            add_spell_cast_time(
                session=session,
                spell_cast_time_value=spell_cast_time_dict.get("number"),
                spell_cast_time_unit=spell_cast_time_dict.get("unit"),
                condition=spell_cast_time_dict.get("condition"),
            )
            for spell_cast_time_dict in spell_dict["time"]
        ]
        logger.debug(
            f"Adding {len(spell_cast_times)} spell cast times to spell {spell_name}"
        )
        spell.spell_cast_times = spell_cast_times
    session.add(spell)
    try:
        session.commit()
    except sqlalchemy.orm.exc.FlushError as e:
        logger.error(f"Error adding spell: {spell_dict['name']}")
        raise e


def get_or_add_area_tag(session: Session, area_tag_short: str) -> AreaTag:
    statement = select(AreaTag).where(
        func.lower(AreaTag.short) == area_tag_short.lower()
    )
    results = session.exec(statement)
    area_tag = results.one_or_none()
    if area_tag is None:
        area_tag = AreaTag(short=area_tag_short, name=SPELL_AREA_TAGS[area_tag_short])
        # session.add(area_tag)
    return area_tag


def get_or_add_creature_type(session: Session, creature_type_name: str) -> CreatureType:
    statement = select(CreatureType).where(
        func.lower(CreatureType.name) == creature_type_name.lower()
    )
    results = session.exec(statement)
    creature_type = results.one_or_none()
    if creature_type is None:
        creature_type = CreatureType(name=creature_type_name)
        # session.add(creature_type)
    return creature_type


def add_spell_component(
    session: Session, spell_component_short: str, spell_component_desc: str = None
) -> SpellComponent:
    spell_component = SpellComponent(short=spell_component_short)
    if spell_component_desc:
        if isinstance(spell_component_desc, dict):
            spell_component.description = spell_component_desc.get("text")
        elif isinstance(spell_component_desc, bool):
            spell_component.description = ""
        else:
            spell_component.description = spell_component_desc
    session.add(spell_component)
    return spell_component


def add_spell_duration(
    session: Session,
    spell_duration_value: int,
    spell_duration_unit: str,
    duration_type: str,
    concentration: bool = False,
    up_to: bool = False,
    ends: list[str] = [],
) -> SpellDuration:
    spell_duration = SpellDuration(
        value=spell_duration_value,
        unit=spell_duration_unit,
        concentration=concentration,
        up_to=up_to,
        duration_type=duration_type,
        ends=ends,
    )
    session.add(spell_duration)
    return spell_duration


def add_spell_duration_end(session: Session, name: str) -> SpellDurationEnd:
    spell_duration_end = SpellDurationEnd(name=name)
    session.add(spell_duration_end)
    return spell_duration_end


def get_or_add_meta_key(session: Session, meta_key: str) -> SpellMetaKey:
    statement = select(SpellMetaKey).where(
        func.lower(SpellMetaKey.key) == meta_key.lower()
    )
    results = session.exec(statement)
    spell_meta_key = results.one_or_none()
    if spell_meta_key is None:
        spell_meta_key = SpellMetaKey(key=meta_key)
        # session.add(spell_meta_key)
    return spell_meta_key


def get_or_add_misc_tag(session: Session, misc_tag: str) -> SpellMiscTag:
    statement = select(SpellMiscTag).where(
        func.lower(SpellMiscTag.name) == misc_tag.lower()
    )
    results = session.exec(statement)
    spell_misc_tag = results.one_or_none()
    if spell_misc_tag is None:
        spell_misc_tag = SpellMiscTag(name=misc_tag)
        # session.add(spell_misc_tag)
    return spell_misc_tag


def add_spell_range(
    session: Session,
    spell_range_value: int,
    spell_range_unit: str,
    range_type: str,
) -> SpellRange:
    spell_range = SpellRange(
        value=spell_range_value, unit=spell_range_unit, range_type=range_type
    )
    session.add(spell_range)
    return spell_range


def add_spell_scaling(
    session: Session, label: str, scaling: dict[str, str]
) -> SpellScaling:
    spell_scaling = SpellScaling(label=label)
    scale_levels = [
        SpellScaleLevel(level=level, dice_string=dice_string)
        for level, dice_string in scaling.items()
    ]
    # session.add_all(scale_levels)
    spell_scaling.scale_levels = scale_levels
    # session.add(spell_scaling)
    return spell_scaling


def add_spell_cast_time(
    session: Session,
    spell_cast_time_value: int,
    spell_cast_time_unit: str,
    condition: str = None,
) -> SpellCastTime:
    spell_cast_time = SpellCastTime(
        value=spell_cast_time_value, unit=spell_cast_time_unit, condition=condition
    )
    # session.add(spell_cast_time)
    return spell_cast_time


# spell school functions
def get_spell_school(session: Session, school_short: str) -> SpellSchool:
    statement = select(SpellSchool).where(
        func.lower(SpellSchool.short) == school_short.lower()
    )
    results = session.exec(statement)
    spell_school = results.one_or_none()
    if spell_school is None:
        logger.error(f"No spell school found for: {school_short}")
        raise KeyError(f"No spell school found for: {school_short}")
    return spell_school


def add_spell_school(
    session: Session, school_short: str, name: str, description
) -> SpellSchool:
    logger.debug(f"Adding spell school: {name}")
    spell_school = SpellSchool(short=school_short, name=name, description=description)
    session.add(spell_school)
    return spell_school
