import logging
from typing import TYPE_CHECKING, Any, Optional, Protocol
from arrow import get
import sqlalchemy

from sqlmodel import Session
from dnd_player_helper.dnd_model.entry.cell_entry import TableCell
from dnd_player_helper.dnd_model.entry.list_entry import ListEntry
from dnd_player_helper.dnd_model.entry.list_item import ListItem

from dnd_player_helper.dnd_model.entry.string_entry import StringEntry
from dnd_player_helper.dnd_model.entry.entry_set import EntrySet
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


class Entry(Protocol):
    def as_dict(self) -> dict:
        ...


def entry_set_from_list(
    session: Session,
    entries: list[str | dict],
    entry_id: Optional[int] = None,
    is_inset: bool = False,
    name: Optional[str] = None,
) -> EntrySet:
    entry_set = EntrySet(entry_id=entry_id, name=name, is_inset=is_inset)
    for i, entry in enumerate(entries):
        entry_type, new_entry = get_entry(entry=entry, entry_id=i, session=session)

        if entry_type == "string":
            entry_set.string_entries.append(new_entry)
            continue

        if entry_type == "list":
            entry_set.list_entries.append(new_entry)
            continue

        if entry_type == "table":
            entry_set.table_entries.append(new_entry)
            continue

        if entry_type == "inset":
            entry_set.child_entry_sets.append(new_entry)
            continue

        if entry_type == "entries":
            entry_set.child_entry_sets.append(new_entry)
            continue

        if entry_type == "options":
            entry_set.list_entries.append(new_entry)

        raise ValueError(f"Unknown entry type {type(entry)}")
    session.add(entry_set)
    return entry_set


def list_entry_from_list(
    session: Session, entries: list[str], name: Optional[str], entry_id: int
) -> ListEntry:
    list_entry = ListEntry(name=name, entry_id=entry_id)
    for i, item in enumerate(entries):
        # get item name and text
        if isinstance(item, str):
            name = None
            text = item
        else:
            name = item.get("name")
            text = item.get("entry")

        string_entry = StringEntry(text=text)
        list_item = ListItem(name=name, entry=string_entry, entry_id=i)

        session.add(string_entry)
        session.add(list_item)
        list_entry.items.append(list_item)

    return list_entry


def table_entry_from_dict(
    session: Session,
    col_labels: list[str],
    rows: list[list[str]],
    name: Optional[str],
    entry_id: int,
) -> TableEntry:
    table_entry = TableEntry(name=name, entry_id=entry_id)

    for col_id, col_label in enumerate(col_labels):
        string_entry = StringEntry(text=col_label)
        new_entry = TableCell(
            entry=string_entry, is_caption=True, row_id=0, col_id=col_id
        )
        session.add(string_entry)
        session.add(new_entry)
        table_entry.cell_entries.append(new_entry)

    for row_id, row in enumerate(rows, start=1):
        for col_id, col in enumerate(row):
            entry_type, cell_entry = get_entry(entry=col, entry_id=-1, session=session)
            if entry_type not in ["string", "cell"]:
                logger.error(
                    f"Expected type StringEntry for cell entry but received type: {type(cell_entry)}"
                )
                raise TypeError(f"Expected type str for cell entry:\n'{cell_entry}'")
            new_entry = TableCell(col_id=col_id, row_id=row_id, entry=cell_entry)
            session.add(cell_entry)
            session.add(new_entry)
            table_entry.cell_entries.append(new_entry)

    return table_entry


def add_entry_set(session: Session, entries: list[str | dict]) -> int:
    try:
        entry_set = entry_set_from_list(session=session, entries=entries)
    except Exception as e:
        logger.error(f"Error getting an entry set from: {entries}")
        raise e
    session.add(entry_set)
    try:
        session.commit()
    except sqlalchemy.exc.ProgrammingError as e:
        logger.error(f"Error commiting the entry set: {entries}")
        raise e
    session.refresh(entry_set)
    return entry_set.id


def add_cell_entry(entry: dict) -> StringEntry:
    # check if there are more than two keys in the dict
    if len(entry.keys()) > 2:
        raise ValueError(f"Cell entry has more than two keys: {entry}")

    cell_dict_map = {"roll": roll_entry_to_str}

    for key, func in cell_dict_map.items():
        if key in entry:
            text = func(entry[key])
            return StringEntry(text=text)
    raise KeyError(f"Unknown cell entry type: {entry}")


def roll_entry_to_str(entry: dict) -> str:
    if "exact" in entry:
        return entry["exact"]
    if "min" in entry and "max" in entry:
        return f"{entry['min']}-{entry['max']}"


def get_entry(entry: dict | str, entry_id: int, session: Session) -> tuple[str, Entry]:
    if isinstance(entry, str):
        new_entry = StringEntry(text=entry, entry_id=entry_id)
        session.add(new_entry)
        return "string", new_entry

    entry_type = entry.get("type", None)

    if entry_type == "list":
        new_entry = list_entry_from_list(
            session=session,
            entries=entry.get("items"),
            name=entry.get("name"),
            entry_id=entry_id,
        )
        session.add(new_entry)
        return entry_type, new_entry

    if entry_type == "table":
        new_entry = table_entry_from_dict(
            session=session,
            col_labels=entry.get("colLabels"),
            rows=entry.get("rows"),
            name=entry.get("name"),
            entry_id=entry_id,
        )
        session.add(new_entry)
        return entry_type, new_entry

    if entry_type == "inset":
        new_entry = entry_set_from_list(
            session=session,
            entries=entry.get("entries"),
            name=entry.get("name"),
            entry_id=entry_id,
            is_inset=True,
        )
        session.add(new_entry)
        return entry_type, new_entry

    if entry_type == "entries":
        new_entry = entry_set_from_list(
            session=session,
            entries=entry.get("entries"),
            name=entry.get("name"),
            entry_id=entry_id,
        )
        session.add(new_entry)
        return entry_type, new_entry

    if entry_type == "options":
        # create a list entry from the options
        list_items = []
        for item in entry.get("entries"):
            for key, value in item.items():
                string_entry = ""
                string_entry += f"{key}: {value}\n"
            list_items.append(string_entry)
        new_entry = list_entry_from_list(
            session=session, entries=list_items, entry_id=entry_id
        )
        session.add(new_entry)
        return entry_type, new_entry

    if entry_type == "cell":
        new_entry = add_cell_entry(entry=entry)
        session.add(new_entry)
        return entry_type, new_entry
