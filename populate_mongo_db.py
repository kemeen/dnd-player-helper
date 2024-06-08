import json
import logging
import os
import pathlib

from dotenv import load_dotenv
from dnd_player_helper.mongo_model.dnd_model import get_database
from pymongo import collection

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

# create console handler and set level to debug
console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# add formatter to console_handler
console_handler.setFormatter(formatter)

# add console_handler to logger
logger.addHandler(console_handler)

load_dotenv('.env')

FEATS_PATH = pathlib.Path(r'C:\software_projects\python\dnd-player-helper\data\feat')
BACKGROUNDS_PATH = pathlib.Path(r'C:\software_projects\python\dnd-player-helper\data\background')
BEASTIARY_PATH = pathlib.Path(r'C:\software_projects\python\dnd-player-helper\data\beastiary\beastiary.json')
BOOK_PATH = pathlib.Path(r'C:\software_projects\python\dnd-player-helper\data\book\book')
ADVENTURE_PATH = pathlib.Path(r'C:\software_projects\python\dnd-player-helper\data\book\adventure')
CLASS_PATH = pathlib.Path(r'C:\software_projects\python\dnd-player-helper\data\class')
LANGUAGE_PATH = pathlib.Path(r'C:\software_projects\python\dnd-player-helper\data\language\all_languages.json')
OPTIONAL_FEATURES_PATH = pathlib.Path(r'C:\software_projects\python\dnd-player-helper\data\optionalfeature')
RACE_PATH = pathlib.Path(r'C:\software_projects\python\dnd-player-helper\data\race')
SKILL_PATH = pathlib.Path(r'C:\software_projects\python\dnd-player-helper\data\skill')
SPELLS_PATH = pathlib.Path(r'C:\software_projects\python\dnd-player-helper\data\spell')
SPELL_LOOKUP_PATH = pathlib.Path(r'C:\software_projects\python\dnd-player-helper\data\spell-lookup')
SUB_RACE_PATH = pathlib.Path(r'C:\software_projects\python\dnd-player-helper\data\sub-race')
ACTIONS_PATH = pathlib.Path(r'C:\software_projects\python\dnd-player-helper\data\tables\actions.json')
ALIGNMENTS_PATH = pathlib.Path(r'C:\software_projects\python\dnd-player-helper\data\tables\alignments.json')
CONDITIONS_PATH = pathlib.Path(r'C:\software_projects\python\dnd-player-helper\data\tables\conditions.json')
DAMAGE_TYPES_PATH = pathlib.Path(r'C:\software_projects\python\dnd-player-helper\data\tables\damage_types.json')
SPELL_SCHOOLS_PATH  = pathlib.Path(r'C:\software_projects\python\dnd-player-helper\data\tables\spell_schools.json')
VEHICLES_PATH = pathlib.Path(r'C:\software_projects\python\dnd-player-helper\data\tables\vehicles.json')
BASE_ITEMS_PATH = pathlib.Path(r'C:\software_projects\python\dnd-player-helper\data\items\base\baseitem')
ITEM_ENTRIES_PATH = pathlib.Path(r'C:\software_projects\python\dnd-player-helper\data\items\base\itemEntry')
ITEM_PROPERTIES_PATH = pathlib.Path(r'C:\software_projects\python\dnd-player-helper\data\items\base\itemProperty')
ITEM_TYPES_PATH = pathlib.Path(r'C:\software_projects\python\dnd-player-helper\data\items\base\itemType')
ITEM_TYPES_ADDITIONAL_ENTRIES_PATH = pathlib.Path(r'C:\software_projects\python\dnd-player-helper\data\items\base\itemTypeAdditionalEntries')
ITEMS_PATH = pathlib.Path(r'C:\software_projects\python\dnd-player-helper\data\items\items\item')
ITEM_GROUPS_PATH = pathlib.Path(r'C:\software_projects\python\dnd-player-helper\data\items\items\itemGroup')
ITEM_MAGIC_VARIANTS_PATH = pathlib.Path(r'C:\software_projects\python\dnd-player-helper\data\items\magicvariants\magicvariant')

def add_documents_from_path(document_path: pathlib.Path, col: collection) -> None:
    for doc in document_path.glob('*.json'):
        with open(doc, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # print(data)
            col.insert_one(data)

def add_beastiary(beast_path: pathlib.Path, col: collection) -> None:
    with open(beast_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for key, val in data.items():
        col.insert_one(val)
        beasts = val.get("monster")
        if beasts:
            logger.info(f"Inserting {len(beasts)} monsters")
            col.insert_many(beasts)

def add_all_languages(lang_path: pathlib.Path, col: collection) -> None:
    with open(lang_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        all_languages = data.get("language")
        if all_languages:
            logger.info(f"Inserting {len(all_languages)} languages")
            col.insert_many(all_languages)

def add_spell_lookup(path: pathlib.Path, col: collection) -> None:
    for file_path in path.glob('*.json'):
        with file_path.open('r', encoding='utf-8') as f:
            data = json.load(f)
            for key, val in data.items():
                val["name"] = key
                col.insert_one(val)

def add_list_from_file(path: pathlib.Path, col: collection, key: str=None, add_fields: dict=None) -> None:
    with path.open('r', encoding='utf-8') as f:
        data = json.load(f)
        if key is None:
            entries = data
        else:
            entries = data.get(key)

        if entries:
            logger.info(f"Inserting {len(entries)} entries")
            if add_fields:
                for entry in entries:
                    entry.update(add_fields)
            col.insert_many(entries)

def add_damage_types(path: pathlib.Path, col: collection) -> None:
    with path.open('r', encoding='utf-8') as f:
        data = json.load(f)
        rows = data.get("rows")
        data.pop("rows")
        data.pop("colStyles")
        entries = []
        for name, desc in rows:
            data["name"] = name
            data["descripton"] = desc
            entries.append(data.copy())
        col.insert_many(entries)

def main():
    db = get_database(user=os.environ.get("MONGODB_USER"), pwd=os.environ.get("MONGODB_PWD"))
    # db.feats.drop()
    # add_documents_from_path(document_path=FEATS_PATH, col=db.feats)
    # db.backgrounds.drop()
    # add_documents_from_path(document_path=BACKGROUNDS_PATH, col=db.backgrounds)
    # db.beastiary.drop()
    # add_beastiary(beast_path=BEASTIARY_PATH, col=db.beastiary)
    # db.books.drop()
    # add_documents_from_path(document_path=BOOK_PATH, col=db.books)
    # db.adventures.drop()
    # add_documents_from_path(document_path=ADVENTURE_PATH, col=db.adventures)
    # db.classes.drop()
    # add_documents_from_path(document_path=CLASS_PATH, col=db.classes)
    # db.languages.drop()
    # add_all_languages(lang_path=LANGUAGE_PATH, col=db.languages)
    # db.optional_features.drop()
    # add_documents_from_path(document_path=OPTIONAL_FEATURES_PATH, col=db.optional_features)
    # db.races.drop()
    # add_documents_from_path(document_path=RACE_PATH, col=db.races)
    # db.skills.drop()
    # add_documents_from_path(document_path=SKILL_PATH, col=db.skills)
    # db.spells.drop()
    # for path in SPELLS_PATH.glob('*'):
    #     if path.is_file():
    #         continue
    #     add_documents_from_path(document_path=path, col=db.spells)
    # db.spell_lookup.drop()
    # add_spell_lookup(path=SPELL_LOOKUP_PATH, col=db.spell_lookup)
    # db.sub_races.drop()
    # add_documents_from_path(document_path=SUB_RACE_PATH, col=db.sub_races)
    # db.actions.drop()
    # add_list_from_file(path=ACTIONS_PATH, col=db.actions, key="action")
    # db.alignments.drop()
    # add_list_from_file(path=ALIGNMENTS_PATH, col=db.alignments, key=None)
    # db.conditions.drop()
    # add_list_from_file(path=CONDITIONS_PATH, col=db.conditions, key="condition", add_fields={"type": "condition"})
    # add_list_from_file(path=CONDITIONS_PATH, col=db.conditions, key="disease", add_fields={"type": "disease"})
    # add_list_from_file(path=CONDITIONS_PATH, col=db.conditions, key="status", add_fields={"type": "status"})
    # db.damage_types.drop()
    # add_damage_types(path=DAMAGE_TYPES_PATH, col=db.damage_types)
    # db.spell_schools.drop()
    # add_list_from_file(path=SPELL_SCHOOLS_PATH, col=db.spell_schools, key=None)
    # db.vehicles.drop()
    # add_list_from_file(path=VEHICLES_PATH, col=db.vehicles, key="vehicle")
    # db.vehicle_upgrades.drop()
    # add_list_from_file(path=VEHICLES_PATH, col=db.vehicle_upgrades, key="vehicleUpgrade")
    db.base_items.drop()
    add_documents_from_path(document_path=BASE_ITEMS_PATH, col=db.base_items)
    db.item_entries.drop()
    add_documents_from_path(document_path=ITEM_ENTRIES_PATH, col=db.item_entries)
    db.item_properties.drop()
    add_documents_from_path(document_path=ITEM_PROPERTIES_PATH, col=db.item_properties)
    db.item_types.drop()
    add_documents_from_path(document_path=ITEM_TYPES_PATH, col=db.item_types)
    db.item_type_additional_entries.drop()
    add_documents_from_path(document_path=ITEM_TYPES_ADDITIONAL_ENTRIES_PATH, col=db.item_type_additional_entries)
    db.items.drop()
    add_documents_from_path(document_path=ITEMS_PATH, col=db.items)
    db.item_groups.drop()
    add_documents_from_path(document_path=ITEM_GROUPS_PATH, col=db.item_groups)
    db.item_magic_variants.drop()
    add_documents_from_path(document_path=ITEM_MAGIC_VARIANTS_PATH, col=db.item_magic_variants)

if __name__ == "__main__":
    main()