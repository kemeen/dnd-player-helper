import logging
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel, Session, select

from dnd_player_helper.dnd_model.links import RaceSizeLink

if TYPE_CHECKING:
    from dnd_player_helper.dnd_model.race import Race

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


class Size(SQLModel, table=True):
    name: str = Field(primary_key=True)
    long_name: str
    races: Optional[list["Race"]] = Relationship(
        back_populates="sizes",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=RaceSizeLink,
    )


def get_size_by_name(size_name: str, session: Session) -> Size:
    size = session.exec(select(Size).where(Size.name == size_name)).one()
    return size
