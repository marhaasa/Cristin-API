import json
import sys
import requests
import pandas as pd
from pandas.io.json import json_normalize


ferdig = False
counter = 1
thisPage = requests.get("https://api.cristin.no/v2/results?institution=7548&per_page=1000")
sys.stdout.write("Arbeider")

rawData = json.loads(thisPage.text)
data = json_normalize(rawData)

while not ferdig:
    nextPage = requests.get(thisPage.links["next"]["url"])
    try:
        if nextPage.links["next"] is not None:
            if nextPage.links["next"]:
                thisPage = nextPage
                counter = counter + 1
                sys.stdout.flush()
                sys.stdout.write(".")
                rawData = json.loads(thisPage.text)
                data = data.append(json_normalize(rawData), sort=True)
    except KeyError:
        rawData = json.loads(nextPage.text)
        data = data.append(json_normalize(rawData), sort=True)
        counter = counter + 1
        sys.stdout.write(" Ferdig!")
        print(f"\nSiste side i API-kallet er: https://api.cristin.no/v2/results?institution=7548&page={counter}&per_page=1000")
        ferdig = True
data.to_excel("publikasjoner.xlsx", index=False)


### GET SPECIFIC PAGE, REMOVE COLUMNS, RENAME COLUMNS, PRINT TO .XLSX ###

""" 
response = requests.get("https://api.cristin.no/v2/results?institution=7548&per_page=1000") 
rawdata = json.loads(response.text)
data = json_normalize(rawdata)
data = data.drop(["original_language", "cristin_result_id", "category.name.en", "url", "channel.title", "contributors.url", "date_published", "journal.name", "part_of.url", "links", "pages.from", "pages.to", "journal.publisher.url", "pages.count", "journal.publisher.name"], axis=1)
data = data.rename({'year_published': 'Publiseringsår', 'category.code' : 'Kategorikode', "title.en" : "Tittel"}, axis=1) 
data = data[["Tittel", "Publiseringsår", "Kategorikode"]]
data.to_excel("publikasjoner.xlsx", index=False)
print("Printing av excel-dokument vellykket")
"""
