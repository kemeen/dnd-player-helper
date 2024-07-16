import logging
import flet as ft
from typing import Any
from dnd_player_helper.theme import text_theme

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# add formatter to console_handler
console_handler.setFormatter(formatter)

# add console_handler to logger
logger.addHandler(console_handler)

INSET = 4
ENTITY_PADDING = ft.padding.only(bottom=10)

def render_entry_set(entries: list[dict[str, Any]], title: str = None, indent: int = 0) -> ft.Container:

    entry_set_column = ft.Column()
    # add title if name is not none
    if title:
        logger.debug(f"name: {title}")
        entry_set_column.controls.append(
            ft.Text(title, style=text_theme.headline_small)
        )

    # add entries
    for entry in entries:
        # render string entry
        if isinstance(entry, str):
            logger.debug(f"rendering string entry")
            content = render_string_entry(entry=entry)
            entry_set_column.controls.append(content)
            continue

        entry_type = entry.get("type")
        logger.debug(f"entry_type: {entry_type}")

        # render inset entry set
        if entry_type == "inset":
            logger.debug(f"rendering inset entry set")
            # entry_set_column.controls.append(ft.Text("TODO Add inset entry render"))
            # continue
            content = render_entry_set(entries=entry, title=entry.get('name'), indent=indent + INSET)
            entry_set_column.controls.append(content)
            continue

        # render entry set
        if entry_type == "entries":
            logger.debug(f"rendering entry set")
            # entry_set_column.controls.append(ft.Text("TODO Add entry set render"))
            # continue
            content = render_entry_set(entries=entry.get('entries'), indent=indent, title=entry.get('name'))
            entry_set_column.controls.append(content)
            continue

        # render table
        if entry_type == "table":
            logger.debug(f"rendering table")
            # entry_set_column.controls.append(ft.Text("TODO Add table render"))
            # continue
            table_container = render_table(table_dict=entry)
            entry_set_column.controls.append(table_container)
            continue

        # render list
        if entry_type == "list":
            logger.debug(f"rendering list")
            list_container = render_list(list_dict=entry)
            entry_set_column.controls.append(list_container)
            continue
        raise ValueError(f"Unknown entry type: {entry_type}")

    # return ft.Container(content=ft.Text("TODO"))
    return ft.Container(content=entry_set_column)

def render_table(table_dict: dict[str, Any]) -> ft.Container:
    root = ft.Column(spacing=0)

    # get caption
    caption = table_dict.get("caption")
    if caption:
        root.controls.append(ft.Text(caption, style=text_theme.headline_small))
        logger.debug(f"caption: {caption}")

    # get column headers
    # TODO add style for column headers
    column_headers = [ft.DataColumn(ft.Text(c)) for c in table_dict.get("colLabels")]

    # get_rows
    rows = table_dict.get("rows")
    
    data_rows = []
    for row in rows:
        data_cells = [ft.DataCell(ft.Text(cell)) for cell in row]
        data_rows.append(ft.DataRow(cells=data_cells))

    table = ft.DataTable(columns=column_headers, rows=data_rows)
    root.controls.append(table)
    return ft.Container(content=root, padding=ENTITY_PADDING)

def render_list(list_dict: dict[str, Any]) -> ft.Container:
    if list_dict is None:
        logger.debug(f"list_dict is None")
        return ft.Container()
    
    logger.debug(f"list_dict: {list_dict}")
    if len(list_dict) == 0:
        logger.debug(f"list_dict is empty")
        return ft.Container()
    
    root = ft.Column(spacing=0)
    # get name
    name = list_dict.get("name")
    logger.debug(f"name: {name}")

    # add title if name is not none
    if name:
        root.controls.append(ft.Text(name, style=text_theme.headline_small))

    # iter through list items
    logger.debug(f"list_dict items: {list_dict["items"]}")
    for item in list_dict["items"]:
        # render string item
        if isinstance(item, str):
            list_item = ft.ListTile(
                leading=ft.Icon(ft.icons.CIRCLE, size=5),
                title=ft.Text(item, style=text_theme.display_small),
                dense=True,
                height=30,
            )
            root.controls.append(list_item)
            continue

        title = item.get("name")
        entries = item.get("entries")
        if entries is None:
            logger.error(f"text is None: {item}")
            raise ValueError("text is None")

        # render string
        text = "\n".join([e for e in entries])
        if title:
            list_item = ft.ListTile(
                # leading=ft.Icon(ft.icons.CIRCLE, size=5),
                title=ft.Text(title, style=text_theme.display_medium),
                subtitle=ft.Text(text, style=text_theme.display_small),
                dense=True,
            )
        else:
            list_item = ft.ListTile(
                leading=ft.Icon(ft.icons.CIRCLE, size=5),
                title=ft.Text(text, style=text_theme.display_small),
                dense=True,
                height=30,
            )
        root.controls.append(list_item)
    return ft.Container(content=root, padding=ENTITY_PADDING)

def render_string_entry(entry: str) -> ft.Container:
    text = ft.Text(entry, style=text_theme.display_small)
    return ft.Container(text, padding=ENTITY_PADDING)
