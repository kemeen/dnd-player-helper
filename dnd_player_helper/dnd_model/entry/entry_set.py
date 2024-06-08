import logging
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from dnd_player_helper.dnd_model.entry.list_entry import ListEntry
    from dnd_player_helper.dnd_model.entry.string_entry import StringEntry
    from dnd_player_helper.dnd_model.entry.table_entry import TableEntry

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


class EntrySet(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    entry_id: Optional[int] = Field(default=None)
    name: Optional[str] = Field(default=None)
    is_inset: Optional[bool] = Field(default=False)
    string_entries: Optional[list["StringEntry"]] = Relationship(
        back_populates="entry_set", sa_relationship_kwargs={"lazy": "selectin"}
    )
    table_entries: Optional[list["TableEntry"]] = Relationship(
        back_populates="entry_set", sa_relationship_kwargs={"lazy": "selectin"}
    )
    list_entries: Optional[list["ListEntry"]] = Relationship(
        back_populates="entry_set", sa_relationship_kwargs={"lazy": "selectin"}
    )
    child_entry_sets: Optional[list["EntrySet"]] = Relationship(
        back_populates="parent_entry_set", sa_relationship_kwargs={"lazy": "selectin"}
    )
    parent_entry_set_id: Optional[int] = Field(default=None, foreign_key="entryset.id")
    parent_entry_set: Optional["EntrySet"] = Relationship(
        back_populates="child_entry_sets",
        sa_relationship_kwargs={"lazy": "selectin", "remote_side": "EntrySet.id"},
    )

    def as_dict(self):
        entries = [entry.as_dict() for entry in self.string_entries]
        entries.extend([entry.as_dict() for entry in self.table_entries])
        entries.extend([entry.as_dict() for entry in self.list_entries])
        entries.extend([entry.as_dict() for entry in self.child_entry_sets])
        entries.sort(key=lambda x: x["entry_id"])
        return {
            "type": "entry_set",
            "name": self.name,
            "is_inset": self.is_inset,
            "entries": entries,
            "entry_id": self.entry_id,
        }
