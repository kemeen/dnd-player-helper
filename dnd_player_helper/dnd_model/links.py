from typing import Optional

from sqlmodel import Field, SQLModel


# ==================================================
# Race Links
# ==================================================
class RaceSkillLink(SQLModel, table=True):
    race_id: Optional[int] = Field(
        default=None, primary_key=True, foreign_key="race.id"
    )
    skill_name: Optional[str] = Field(
        default=None, primary_key=True, foreign_key="skill.name"
    )


class RaceWeaponProficiencyLink(SQLModel, table=True):
    race_id: Optional[int] = Field(
        default=None, primary_key=True, foreign_key="race.id"
    )
    weapon_id: Optional[int] = Field(
        default=None, primary_key=True, foreign_key="weapon.id"
    )


class RaceArmorProficiencyLink(SQLModel, table=True):
    race_id: Optional[int] = Field(
        default=None, primary_key=True, foreign_key="race.id"
    )
    armor_id: Optional[int] = Field(
        default=None, primary_key=True, foreign_key="armor.id"
    )


class RaceSizeLink(SQLModel, table=True):
    race_id: Optional[int] = Field(
        default=None, primary_key=True, foreign_key="race.id"
    )
    size_name: Optional[str] = Field(
        default=None, primary_key=True, foreign_key="size.name"
    )


# ==================================================
# Skill Links
# ==================================================
class SkillChoiceSkillLink(SQLModel, table=True):
    skill_choice_id: Optional[int] = Field(
        default=None, primary_key=True, foreign_key="skillchoice.id"
    )
    skill_name: Optional[str] = Field(
        default=None, primary_key=True, foreign_key="skill.name"
    )


# ==================================================
# Language Links
# ==================================================
class LanguageProficiencyOptionLanguageLink(SQLModel, table=True):
    language_proficiency_option_id: Optional[int] = Field(
        default=None, primary_key=True, foreign_key="languageproficiencyoption.id"
    )
    language_id: Optional[str] = Field(
        default=None, primary_key=True, foreign_key="language.id"
    )


class LanguageProficiencyOptionDialectLink(SQLModel, table=True):
    language_proficiency_option_id: Optional[int] = Field(
        default=None, primary_key=True, foreign_key="languageproficiencyoption.id"
    )
    dialect_name: Optional[str] = Field(
        default=None, primary_key=True, foreign_key="dialect.name"
    )


class LanguageLanguageChoiceLink(SQLModel, table=True):
    language_id: Optional[int] = Field(
        default=None, primary_key=True, foreign_key="language.id"
    )
    language_choice_id: Optional[str] = Field(
        default=None, primary_key=True, foreign_key="languagechoice.id"
    )


class DialectLanguageChoiceLink(SQLModel, table=True):
    dialect_name: Optional[str] = Field(
        default=None, primary_key=True, foreign_key="dialect.name"
    )
    language_choice_id: Optional[str] = Field(
        default=None, primary_key=True, foreign_key="languagechoice.id"
    )


# ==================================================
# Item Links
# ==================================================
class ItemPropertyLink(SQLModel, table=True):
    item_id: int = Field(primary_key=True, default=None, foreign_key="item.id")
    item_property_abbreviation: str = Field(
        primary_key=True, default=None, foreign_key="itemproperty.abbreviation"
    )


class WeaponPropertyLink(SQLModel, table=True):
    weapon_id: int = Field(primary_key=True, default=None, foreign_key="weapon.id")
    item_property_abbreviation: str = Field(
        primary_key=True, default=None, foreign_key="itemproperty.abbreviation"
    )


class WeaponChoiceWeaponLink(SQLModel, table=True):
    weapon_choice_id: int = Field(
        primary_key=True, default=None, foreign_key="weaponchoice.id"
    )
    weapon_id: int = Field(primary_key=True, default=None, foreign_key="weapon.id")


class FeatArmorProficiencyLink(SQLModel, table=True):
    feat_id: int = Field(primary_key=True, default=None, foreign_key="feat.id")
    armor_id: int = Field(primary_key=True, default=None, foreign_key="armor.id")


# ==================================================
# Class Links
# ==================================================
class ClassArmorProficiencyLink(SQLModel, table=True):
    class_name: str = Field(primary_key=True, default=None, foreign_key="dndclass.name")
    armor_id: int = Field(primary_key=True, default=None, foreign_key="armor.id")


class ClassToolProficiencyLink(SQLModel, table=True):
    class_name: str = Field(primary_key=True, default=None, foreign_key="dndclass.name")
    item_id: int = Field(primary_key=True, default=None, foreign_key="item.id")


class ClassWeaponProficiencyLink(SQLModel, table=True):
    class_name: str = Field(primary_key=True, default=None, foreign_key="dndclass.name")
    weapon_id: str = Field(primary_key=True, default=None, foreign_key="weapon.id")


class ClassSkillLink(SQLModel, table=True):
    class_name: str = Field(primary_key=True, default=None, foreign_key="dndclass.name")
    skill_name: str = Field(primary_key=True, default=None, foreign_key="skill.name")


class ClassSavingThrowLink(SQLModel, table=True):
    class_name: str = Field(primary_key=True, default=None, foreign_key="dndclass.name")
    ability_name: str = Field(
        primary_key=True, default=None, foreign_key="ability.name"
    )


# ==================================================
# Beast Links
# ==================================================
# class BeastActionTagBeastLink(SQLModel, table=True):
#     beast_id: int = Field(default=None, foreign_key="beast.id", primary_key=True)
#     tag: str = Field(default=None, foreign_key="beastactiontag.tag", primary_key=True)


# class BeastWeaponLink(SQLModel, table=True):
#     beast_id: int = Field(default=None, foreign_key="beast.id", primary_key=True)
#     weapon_id: int = Field(default=None, foreign_key="weapon.id", primary_key=True)


# class BeastConditionImmunityLink(SQLModel, table=True):
#     beast_id: int = Field(default=None, foreign_key="beast.id", primary_key=True)
#     condition_name: str = Field(
#         default=None, foreign_key="condition.name", primary_key=True
#     )


# class BeastTypeGroupLink(SQLModel, table=True):
#     beast_type_name: str = Field(
#         default=None, foreign_key="beasttype.name", primary_key=True
#     )
#     type_group_name: str = Field(
#         default=None, foreign_key="beastgroup.name", primary_key=True
#     )


# ==================================================
# Spell Links
# ==================================================
class SpellDamageImmunityLink(SQLModel, table=True):
    spell_id: int = Field(default=None, foreign_key="spell.id", primary_key=True)
    damage_type_name: str = Field(
        default=None, foreign_key="damagetype.name", primary_key=True
    )


class SpellAbilityCheckLink(SQLModel, table=True):
    spell_id: int = Field(default=None, foreign_key="spell.id", primary_key=True)
    ability_name: str = Field(
        default=None, foreign_key="ability.name", primary_key=True
    )


class SpellCreatureTypeLink(SQLModel, table=True):
    spell_id: int = Field(default=None, foreign_key="spell.id", primary_key=True)
    creature_type_name: str = Field(
        default=None, foreign_key="creaturetype.name", primary_key=True
    )


class SpellAreaTagLink(SQLModel, table=True):
    spell_id: int = Field(default=None, foreign_key="spell.id", primary_key=True)
    area_tag_short: str = Field(
        default=None, foreign_key="areatag.short", primary_key=True
    )


class SpellConditionImmunityLink(SQLModel, table=True):
    spell_id: int = Field(default=None, foreign_key="spell.id", primary_key=True)
    condition_name: str = Field(
        default=None, foreign_key="condition.name", primary_key=True
    )


class SpellConditionInflictLink(SQLModel, table=True):
    spell_id: int = Field(default=None, foreign_key="spell.id", primary_key=True)
    condition_name: str = Field(
        default=None, foreign_key="condition.name", primary_key=True
    )


class SpellDamageInflictsLink(SQLModel, table=True):
    spell_id: int = Field(default=None, foreign_key="spell.id", primary_key=True)
    damage_type_name: str = Field(
        default=None, foreign_key="damagetype.name", primary_key=True
    )


class SpellDamageResistLink(SQLModel, table=True):
    spell_id: int = Field(default=None, foreign_key="spell.id", primary_key=True)
    damage_type_name: str = Field(
        default=None, foreign_key="damagetype.name", primary_key=True
    )


class SpellDamageVulnerableLink(SQLModel, table=True):
    spell_id: int = Field(default=None, foreign_key="spell.id", primary_key=True)
    damage_type_name: str = Field(
        default=None, foreign_key="damagetype.name", primary_key=True
    )


class SpellMetaKeyLink(SQLModel, table=True):
    spell_id: int = Field(default=None, foreign_key="spell.id", primary_key=True)
    meta_key_name: str = Field(
        default=None, foreign_key="spellmetakey.key", primary_key=True
    )


class SpellMiscTagLink(SQLModel, table=True):
    spell_id: int = Field(default=None, foreign_key="spell.id", primary_key=True)
    misc_tag_name: str = Field(
        default=None, foreign_key="spellmisctag.name", primary_key=True
    )


class SpellSavingThrowLink(SQLModel, table=True):
    spell_id: int = Field(default=None, foreign_key="spell.id", primary_key=True)
    ability_name: str = Field(
        default=None, foreign_key="ability.name", primary_key=True
    )


class SpellDurationEndLink(SQLModel, table=True):
    spell_duration_id: int = Field(
        default=None, foreign_key="spellduration.id", primary_key=True
    )
    duration_end_name: str = Field(
        default=None, foreign_key="spelldurationend.name", primary_key=True
    )


class SpellChoiceAbilityLink(SQLModel, table=True):
    spell_choice_id: int = Field(
        default=None, foreign_key="spellchoice.id", primary_key=True
    )
    ability_name: str = Field(
        default=None, foreign_key="ability.name", primary_key=True
    )
