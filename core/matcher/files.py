import json

with open("data/passions.json", "r", encoding="utf-8") as f:
    passions = json.load(f)

with open("data/occupations.json", "r", encoding="utf-8") as f:
    occupations = json.load(f)