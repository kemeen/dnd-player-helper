import logging
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from dnd_player_helper.dnd_model.links import (
    DialectLanguageChoiceLink,
    LanguageLanguageChoiceLink,
    LanguageProficiencyOptionDialectLink,
    LanguageProficiencyOptionLanguageLink,
)

if TYPE_CHECKING:
    from dnd_player_helper.dnd_model.race import Race
    from dnd_player_helper.dnd_model.feat.feat import Feat

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


class Language(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    script: Optional[str] = Field(default=None)
    type: str
    srd: Optional[bool] = Field(default=False)
    basic_rules: Optional[bool] = Field(default=False)
    source: Optional[str] = Field(default=None)
    entry_set_id: Optional[int] = Field(default=None, foreign_key="entryset.id")
    typical_speakers: list["TypicalSpeakers"] = Relationship(
        back_populates="language", sa_relationship_kwargs={"lazy": "selectin"}
    )
    dialects: Optional[list["Dialect"]] = Relationship(
        back_populates="language", sa_relationship_kwargs={"lazy": "selectin"}
    )
    proficiency_options: Optional[list["LanguageProficiencyOption"]] = Relationship(
        back_populates="known_languages",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=LanguageProficiencyOptionLanguageLink,
    )
    language_choices: Optional[list["LanguageChoice"]] = Relationship(
        back_populates="languages",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=LanguageLanguageChoiceLink,
    )


class TypicalSpeakers(SQLModel, table=True):
    language_id: Optional[int] = Field(primary_key=True, foreign_key="language.id")
    name: str = Field(primary_key=True)
    language: Language = Relationship(
        back_populates="typical_speakers", sa_relationship_kwargs={"lazy": "selectin"}
    )


class Dialect(SQLModel, table=True):
    name: str = Field(primary_key=True)
    language_id: Optional[int] = Field(primary_key=True, foreign_key="language.id")
    language: Language = Relationship(
        back_populates="dialects", sa_relationship_kwargs={"lazy": "selectin"}
    )
    language_choices: list["LanguageChoice"] = Relationship(
        back_populates="dialects",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=DialectLanguageChoiceLink,
    )
    language_proficiency_options: Optional[
        list["LanguageProficiencyOption"]
    ] = Relationship(
        back_populates="known_dialects",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=LanguageProficiencyOptionDialectLink,
    )


class LanguageProficiencyOption(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    race_id: Optional[int] = Field(default=None, foreign_key="race.id")
    race: Optional["Race"] = Relationship(
        back_populates="language_proficiency_options",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    known_languages: Optional[list[Language]] = Relationship(
        back_populates="proficiency_options",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=LanguageProficiencyOptionLanguageLink,
    )
    known_dialects: Optional[list[Dialect]] = Relationship(
        back_populates="language_proficiency_options",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=LanguageProficiencyOptionDialectLink,
    )
    language_choices: Optional[list["LanguageChoice"]] = Relationship(
        back_populates="language_proficiency_option",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    feat_id: Optional[int] = Field(default=None, foreign_key="feat.id")
    feat: Optional["Feat"] = Relationship(


class LanguageChoice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    language_proficency_option_id: Optional[int] = Field(
        default=None, foreign_key="languageproficiencyoption.id"
    )
    count: int
    language_proficiency_option: LanguageProficiencyOption = Relationship(
        back_populates="language_choices", sa_relationship_kwargs={"lazy": "selectin"}
    )
    languages: list["Language"] = Relationship(
        back_populates="language_choices",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=LanguageLanguageChoiceLink,
    )
    dialects: list["Dialect"] = Relationship(
        back_populates="language_choices",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=DialectLanguageChoiceLink,
    )


def load_language(json_file: str) -> dict[str, Any]:
    path = pathlib.Path(json_file)
    with path.open("r") as f:
        json_data = json.load(f)

    return json_data


def load_languages(json_file: pathlib.Path) -> list[dict[str, Any]]:
    with json_file.open("r") as f:
        json_data = json.load(f)
    return json_data["language"]


def get_language_by_name(name: str, session: Session) -> Optional[Language]:
    statement = select(Language).where(func.lower(Language.name) == name.lower())
    results = session.exec(statement).all()
    if len(results) == 0:
        logger.debug(f"Language {name} not found.")
        return None
    if len(results) > 1:
        logger.warning(f"Multiple languages with name {name} found.")

        # return if language is SRD
        for language in results:
            if language.srd:
                return language

        # return if language is basic rules
        for language in results:
            if language.basic_rules:
                return language

        # return if language is standard
        for language in results:
            if language.type == "standard":
                return language

    return results[0]


def get_dialect_by_name(name: str, session: Session) -> Optional[Dialect]:
    statement = select(Dialect).where(func.lower(Dialect.name) == name.lower())
    result = session.exec(statement).one_or_none()
    if result is None:
        logger.debug(f"Dialect {name} not found.")
    return result


def get_languages_by_type(type: str, session: Session) -> list[Language]:
    statement = select(Language).where(Language.type == type)
    results = session.exec(statement).all()
    return results


def add_languages(
    race_dict: dict[str, any],
    race: "Race",
    session: Session,
) -> None:
    # check if language proficiencies exist
    language_proficiencies = race_dict.get("languageProficiencies", None)
    if language_proficiencies is None:
        return

    # language_proficiencies are always a list of dicts, most likely a single dict in the list
    # iter over language proficiencies
    # if there is more than one language proficiency, it is a choose between!
    logger.debug(f"Language proficiencies: {language_proficiencies}")
    options = []
    for lang_dict in language_proficiencies:
        # key, value pairs can be
        choices = []
        known_languages = []
        known_dialects = []
        for key, val in lang_dict.items():
            # anyStandard, anyExotic: int defining how any standard languages can be picked
            if key in ["anyStandard", "anyExotic"]:
                languages = get_languages_by_type(type=key, session=session)
                language_choice = LanguageChoice(count=val, languages=languages)
                session.add(language_choice)
                choices.append(language_choice)
                continue

            # other: bool meaning any language of type other
            if key == "other":
                languages = get_languages_by_type(type=key, session=session)
                language_choice = LanguageChoice(count=1, languages=languages)
                session.add(language_choice)
                choices.append(language_choice)
                continue

            # choose: dict with keys count and from meaning you can choose "count" languages from "from"
            if key == "choose":
                count = val.get("count", 1)
                names = val.get("from", None)
                if names is None:
                    logger.error(f"Choose language {key} has no from key.")
                    continue
                languages = []
                dialects = []
                for name in names:
                    if name == "other":
                        languages.extend(
                            get_languages_by_type(type="other", session=session)
                        )
                        continue
                    language = get_language_by_name(name=name, session=session)
                    dialect = get_dialect_by_name(name=name, session=session)
                    if language:
                        languages.append(language)
                        continue

                    if dialect:
                        dialects.append(dialect)
                        continue
                    logger.error(f"Language {name} not found.")

                # languages = [get_language_by_name(name=name, session=session)]
                language_choice = LanguageChoice(
                    count=count, languages=languages, dialects=dialects
                )
                session.add(language_choice)
                choices.append(language_choice)
                continue

            name = key
            # language_name:True
            language = get_language_by_name(name=name, session=session)
            if language:
                known_languages.append(language)
                continue

            # dialect_name:True
            dialect = get_dialect_by_name(name=name, session=session)
            if dialect:
                known_dialects.append(dialect)
                continue
            logger.error(f"Language {name} not found.")
        try:
            proficiency = LanguageProficiencyOption(
                known_languages=known_languages,
                known_dialects=known_dialects,
                language_choices=choices,
            )
        except KeyError as e:
            logger.debug(f"known languages: {known_languages}")
            logger.debug(f"language choices: {choices}")
            logger.error(f"Error adding language proficiency: {e}")
            raise e
        session.add(proficiency)
        options.append(proficiency)

    # add language proficiency options to race and commit to DB
    race.language_proficiency_options = options
    session.add(race)
    session.commit()

    # for proficiency_dict in language_proficiencies:
    #     pass


def add_language(language_dict: dict[str, Any], session: Session) -> None:
    typical_speakers = [
        TypicalSpeakers(language_name=language_dict["name"], name=typical_speaker)
        for typical_speaker in language_dict.get("typical_speakers", [])
    ]
    dialects = [
        Dialect(language_name=language_dict["name"], name=dialect)
        for dialect in language_dict.get("dialects", [])
    ]
    # add entries to language
    entries = language_dict.get("entries", None)
    entry_set_id = None
    if entries:
        entry_set_id = add_entry_set(session=session, entries=entries)
    language = Language(
        name=language_dict["name"],
        script=language_dict.get("script", None),
        type=language_dict.get("type", "other"),
        source=language_dict.get("source", None),
        srd=language_dict.get("srd", False),
        basic_rules=language_dict.get("basic_rules", False),
        typical_speakers=typical_speakers,
        dialects=dialects,
        entry_set_id=entry_set_id,
    )
    session.add(language)
    session.commit()
