import requests
import zipfile
import io
import numpy as np
import pandas as pd
import sklearn as sk

# Download the zip from mtgjson
r = requests.get("http://mtgjson.com/json/AllCards-x.json.zip")
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall("./")

json = ""

with open("AllCards-x.json") as f:
    json = pd.read_json(f.read())
