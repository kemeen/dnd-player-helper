import logging
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from dnd_player_helper.dnd_model.entry.cell_entry import TableCell
    from dnd_player_helper.dnd_model.entry.entry_set import EntrySet

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


class TableEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    entry_id: Optional[int] = Field(default=None)
    caption: Optional[str] = Field(default=None)
    cell_entries: Optional[list["TableCell"]] = Relationship(
        back_populates="table", sa_relationship_kwargs={"lazy": "selectin"}
    )
    entry_set_id: Optional[int] = Field(default=None, foreign_key="entryset.id")
    entry_set: Optional["EntrySet"] = Relationship(
        back_populates="table_entries", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def as_dict(self):
        return {
            "type": "table",
            "entry_id": self.entry_id,
            "caption": self.caption,
            "cells": [cell.as_dict() for cell in self.cell_entries],
        }
