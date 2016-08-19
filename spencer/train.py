import requests
import json
import pprint
import zipfile
import io
import numpy as np
import pandas as pd
import sklearn as sk

# Download the zip from mtgjson
r = requests.get("http://mtgjson.com/json/AllCards-x.json.zip")
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall("./")

raw_json = ""

with open("AllCards-x.json") as f:
    raw_json = json.load(f) 
    # df = pd.read_json(f.read())

# AllCards-x.json returns the cards as a giant JSON object, here we turn them
# into an array of dicts and convert printings to printing removing printings
# Since working with multiple printings will be easier as seperate rows.
cards = []
for name, card in raw_json.items():
    for printing in card['printings']:
        c = card.copy()

        # Convert printing to singular and drop the unneeded column.
        c['printing'] = printing
        c.pop('printings', None) 

        # Split the legalities out into 0, 1, or 2 and add a key for each legality
        legalities = c.pop('legalities', None)
        # If there are no legalities it's not a card we need to worry about.
        if legalities == None:
            print("Skipping not legal.")
            pprint.pprint(c)
            continue

        for l in legalities:
            if l['legality'] == "Banned":
                c[l['format']] = 0
            elif l['legality'] == "Restricted":
                c[l['format']] = 2
            else:
                c[l['format']] = 1

        cards.append(c)
            
df = pd.DataFrame(cards)
df.drop('imageName', axis=1, inplace=True)
df.drop('rulings', axis=1, inplace=True)

print(df.to_string())
