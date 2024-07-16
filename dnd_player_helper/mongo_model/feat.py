import json
import pathlib
from pymongo import database


def add_feats(feats_path: pathlib.Path, db: database):
    feats_collection = db.feats
    for feat in feats_path.glob('*.json'):
        with open(feat, 'r') as f:
            data = json.load(f)
            print(data)
            feats_collection.insert_one(data)

