import logging
from typing import TYPE_CHECKING, Optional
from sqlmodel import Relationship, SQLModel, Field

if TYPE_CHECKING:
    from dnd_player_helper.dnd_model.entry.table_entry import ListEntry
    from dnd_player_helper.dnd_model.entry.string_entry import StringEntry

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


class ListItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    entry_id: Optional[int] = Field(default=None)
    name: Optional[str] = Field(default=None)
    entry: Optional["StringEntry"] = Relationship(
        back_populates="list_item", sa_relationship_kwargs={"lazy": "selectin"}
    )
    list_entry_id: Optional[int] = Field(default=None, foreign_key="listentry.id")
    list_entry: Optional["ListEntry"] = Relationship(
        back_populates="items", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def as_dict(self):
        return {
            "type": "list_item",
            "name": self.name,
            "entry": self.entry.as_dict(),
            "entry_id": self.entry_id,
        }
