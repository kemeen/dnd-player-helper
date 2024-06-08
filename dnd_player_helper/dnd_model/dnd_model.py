import logging
import pathlib
from typing import Any
from sqlmodel import SQLModel, create_engine, Session, select

from dnd_player_helper.dnd_model.spell import Spell


from .size import Size
from .skill import Skill
from .dnd_class import DNDClass
from .damage_type import DamageType
from .ability import Ability
from .item import Item, Weapon, Armor, ItemType, ItemProperty
from .height_and_weight import Height, Weight
from .language import Language, Dialect, LanguageChoice
from .race import (
    Race,
)

# from .beast import Beast, BeastAction, BeastActionTag, BeastAlias
from .condition import Condition
from .alignment import Alignment

# from .spell import Spell, AreaTag, SpellSchool, SpellCastTime, SpellComponent
from .entry import *


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


SQLITE_FILE_NAME = "dnd.db"
SQLITE_URL = f"sqlite:///{SQLITE_FILE_NAME}"
# DND_ENGINE = create_engine(SQLITE_URL, echo=True)


class DNDModel:
    def __init__(self, echo: bool = True) -> None:
        self.engine = create_engine(SQLITE_URL, echo=echo)

    def get_session(self) -> Session:
        return Session(self.engine)

    def delete_db(self) -> None:
        db_file = pathlib.Path(SQLITE_FILE_NAME)
        db_file.unlink(missing_ok=True)

    def create_db_and_tables(self) -> None:
        SQLModel.metadata.create_all(self.engine)

    def get_all_races(self, session: Session = None) -> list[Race]:
        if session:
            statement = select(Race)
            results = session.exec(statement)
            races = results.all()
            return races
        with Session(self.engine) as session:
            statement = select(Race)
            results = session.exec(statement)
            races = results.all()
        return races

    def get_all_sizes(self, session: Session = None) -> list[Size]:
        if session:
            statement = select(Size)
            results = session.exec(statement)
            sizes = results.all()
            return sizes
        with Session(self.engine) as session:
            statement = select(Size)
            results = session.exec(statement)
            sizes = results.all()
        return sizes

    def get_all_skills(self, session: Session = None) -> list[Skill]:
        if session:
            statement = select(Skill)
            results = session.exec(statement)
            skills = results.all()
            return skills
        with Session(self.engine) as session:
            statement = select(Skill)
            results = session.exec(statement)
            skills = results.all()
        return skills

    # Spell related
    def get_all_spells(self, session: Session) -> list[Spell]:
        statement = select(Spell)
        results = session.exec(statement, execution_options={"compiled_cache": None})
        spells = results.all()
        return spells

    def get_spell_by_id(self, spell_id: int, session: Session = None) -> dict:
        if session:
            statement = select(Spell).where(Spell.id == spell_id)
            results = session.exec(
                statement, execution_options={"compiled_cache": None}
            )
            spell = results.one()
            return spell
        with Session(self.engine) as session:
            statement = select(Spell).where(Spell.id == spell_id)
            results = session.exec(statement)
            spell = results.one()
        return spell.to_dict()

    def get_entries_by_spell_id(self, spell_id: int) -> dict[str, Any]:
        with Session(self.engine) as session:
            spell = self.get_spell_by_id(spell_id=spell_id, session=session)
            if spell.entry_set_id is None:
                return
            entry_set = self.get_entry_set_by_id(
                entry_set_id=spell.entry_set_id, session=session
            )
            return entry_set.as_dict()

    def get_race_by_id(self, race_id: int, session: Session) -> Race:
        statement = select(Race).where(Race.id == race_id)
        results = session.exec(statement)
        race = results.one()
        return race

    def get_race_name_by_race_id(self, race_id: int) -> str:
        with Session(self.engine) as session:
            race = self.get_race_by_id(race_id=race_id, session=session)
            return race.name

    def get_race_sizes_by_race_id(self, race_id: int) -> list[str]:
        with Session(self.engine) as session:
            race = self.get_race_by_id(race_id=race_id, session=session)
            return [item.name for item in race.sizes]

    def get_race_ages_by_race_id(self, race_id: int) -> dict[str, int]:
        with Session(self.engine) as session:
            race = self.get_race_by_id(race_id=race_id, session=session)
            ages_dict = {age.age_type: age.age_in_years for age in race.ages}
            return ages_dict

    def get_race_weapon_proficiencies_by_race_id(self, race_id: int) -> list[str]:
        with Session(self.engine) as session:
            race = self.get_race_by_id(race_id=race_id, session=session)
            return [weapon.name for weapon in race.weapon_proficiencies]

    def get_race_ids_and_names(self) -> list[tuple[int, str]]:
        return [(r.id, f"{r.name}-{r.source}") for r in self.get_all_races()]

    def get_spell_ids_and_names(self) -> list[tuple[int, str]]:
        with Session(self.engine) as session:
            return [
                (s.id, f"{s.name} ({s.source})")
                for s in self.get_all_spells(session=session)
            ]

    def get_race_entries_by_race_id(self, race_id: int) -> dict[str, dict]:
        with Session(self.engine) as session:
            race = self.get_race_by_id(race_id=race_id, session=session)
            if race.entry_set_id is None:
                return
            entry_set = self.get_entry_set_by_id(
                entry_set_id=race.entry_set_id, session=session
            )
            return entry_set.as_dict()

    def get_entry_set_by_id(self, entry_set_id: int, session: Session) -> EntrySet:
        statement = select(EntrySet).where(EntrySet.id == entry_set_id)
        results = session.exec(statement)
        entry_set = results.one()
        return entry_set
