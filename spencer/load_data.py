import io
import json
import zipfile

import requests
from pymongo import MongoClient

client = MongoClient()
db = client.cards
magic = db.magic

r = requests.get("http://mtgjson.com/json/AllCards-x.json.zip")
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall("./")

with open("AllCards-x.json") as f:
    raw_json = json.load(f)

cards = [card for name, card in raw_json.items()]
magic.insert_many(cards)
