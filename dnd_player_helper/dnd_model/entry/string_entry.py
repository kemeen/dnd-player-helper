import logging
from typing import TYPE_CHECKING, Optional

from sqlmodel import Relationship, SQLModel, Field

if TYPE_CHECKING:
    from dnd_player_helper.dnd_model.entry.cell_entry import TableCell
    from dnd_player_helper.dnd_model.entry.entry_set import EntrySet
    from dnd_player_helper.dnd_model.entry.list_item import ListItem

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


class StringEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    entry_id: Optional[int] = Field(default=None)
    text: Optional[str] = Field(default=None)
    entry_set_id: Optional[int] = Field(default=None, foreign_key="entryset.id")
    entry_set: Optional["EntrySet"] = Relationship(
        back_populates="string_entries", sa_relationship_kwargs={"lazy": "selectin"}
    )
    list_item_id: Optional[int] = Field(default=None, foreign_key="listitem.id")
    list_item: Optional["ListItem"] = Relationship(
        back_populates="entry", sa_relationship_kwargs={"lazy": "selectin"}
    )
    table_cell_id: Optional[int] = Field(default=None, foreign_key="tablecell.id")
    table_cell: Optional["TableCell"] = Relationship(
        back_populates="entry", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def as_dict(self):
        return {"type": "string", "entry_id": self.entry_id, "entry": self.text}
