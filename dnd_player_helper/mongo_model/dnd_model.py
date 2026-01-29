import os
from typing import Any
from dotenv import find_dotenv, load_dotenv
from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId
from pymongo.server_api import ServerApi
from pydantic import BaseModel

load_dotenv(find_dotenv())

class DnDModel(BaseModel):
    uri: str
    db_name: str

    def get_database(self):
        # Create a new client and connect to the server
        client = MongoClient(self.uri, server_api=ServerApi('1'))
        return client[self.db_name]
    
    def get_all_spells(self) -> list[dict]:
        db = self.get_database()
        spells = db.spells
        return spells.find().sort( { "name": 1 } )

    def get_spell_by_id(self, spell_id: str) -> dict:
        _id = ObjectId(spell_id)
        db = self.get_database()
        spells = db.spells
        spell = spells.find_one({"_id": _id})
        return spell
    
    def get_spell_ids_and_names(self) -> list[tuple[int, str]]:
        spells = self.get_all_spells()
        spell_list = [
            (s["_id"], f"{s["name"]} ({s["source"]})")
            for s in spells
        ]
        return spell_list
    
    def get_entries_by_spell_id(self, spell_id: int) -> list[dict[str, Any]]:
        spell = self.get_spell_by_id(spell_id=spell_id)
        entries = spell.get("entries", [])
        entries_higher_level = spell.get("entriesHigherLevel", [])
        entries.extend(entries_higher_level)
        return entries


if __name__ == "__main__":
    model = DnDModel(uri="mongodb://localhost:27017", db_name="session_zero")   
    try:
        db = model.get_database(user=os.environ.get("MONGODB_USER"), pwd=os.environ.get("MONGODB_PWD"))
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    feats = db.feats
    for f in feats.find():
        print(f)

