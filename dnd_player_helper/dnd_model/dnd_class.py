from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING, Optional

from dnd_player_helper.dnd_model.links import (
    ClassArmorProficiencyLink,
    ClassSavingThrowLink,
    ClassSkillLink,
    ClassToolProficiencyLink,
    ClassWeaponProficiencyLink,
)


if TYPE_CHECKING:
    from dnd_player_helper.dnd_model.ability import Ability
    from dnd_player_helper.dnd_model.skill import Skill, SkillChoice
    from dnd_player_helper.dnd_model.item import Armor, Weapon
    from dnd_player_helper.dnd_model.item import Item


class DNDClass(SQLModel, table=True):
    name: str = Field(primary_key=True)
    spellcasting_ability: Optional[str]
    hit_dice: str
    saving_throws: Optional[list["Ability"]] = Relationship(
        back_populates="classes",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=ClassSavingThrowLink,
    )
    skill_proficiencies: Optional[list["Skill"]] = Relationship(
        back_populates="classes",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=ClassSkillLink,
    )
    skill_choices: Optional[list["SkillChoice"]] = Relationship(
        back_populates="dnd_class",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    tool_proficiencies: Optional[list["Item"]] = Relationship(
        back_populates="classes",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=ClassToolProficiencyLink,
    )
    weapon_proficiencies: Optional[list["Weapon"]] = Relationship(
        back_populates="classes",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=ClassWeaponProficiencyLink,
    )
    armor_proficiencies: Optional[list["Armor"]] = Relationship(
        back_populates="classes",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=ClassArmorProficiencyLink,
    )


# def load_class(json_file: str) -> DNDClass:
#     path = pathlib.Path(json_file)
#     with path.open("r") as f:
#         json_data = json.load(f)

#     class_dict = read_dict(input_dict=json_data, key_map=KEY_MAP)
#     # print(class_dict.keys())
#     # features adjustment
#     try:
#         if isinstance(class_dict["features"], list):
#             class_dict["features"] = [
#                 (f["name"], f["level"]) for f in class_dict["features"]
#             ]
#     except KeyError:
#         pass
#     return DNDClass(**class_dict)


# def read_dict(
#     input_dict: dict[str, Any],
#     key_map: dict[str, str],
#     output_dict: dict[str, str] = dict(),
# ) -> None:
#     for key, val in key_map.items():
#         if key in ["class"]:
#             subdict = read_dict(
#                 input_dict=input_dict[key][0], key_map=val, output_dict=output_dict
#             )
#             output_dict.update(subdict)
#             continue

#         input_val = input_dict.get(key, None)
#         if input_val is None:
#             continue

#         output_dict[val] = input_val

#     return output_dict
