import logging
from typing import TYPE_CHECKING, Optional
from sqlmodel import Relationship, SQLModel, Field

if TYPE_CHECKING:
    from dnd_player_helper.dnd_model.entry.table_entry import TableEntry
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


class TableCell(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    col_id: Optional[int] = Field(default=None)
    row_id: Optional[int] = Field(default=None)
    entry: Optional["StringEntry"] = Relationship(
        back_populates="table_cell", sa_relationship_kwargs={"lazy": "selectin"}
    )
    is_caption: Optional[bool] = Field(default=False)
    table_id: Optional[int] = Field(default=None, foreign_key="tableentry.id")
    table: Optional["TableEntry"] = Relationship(
        back_populates="cell_entries", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def as_dict(self):
        return {
            "type": "cell",
            "row": self.row_id,
            "col": self.col_id,
            "entry": self.entry.text,
        }
