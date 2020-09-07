import json
import sys
import requests
import pandas as pd
from pandas.io.json import json_normalize

### Set desired institution ###
institution = 7548


done = False
counter = 1
thisPage = requests.get(f"https://api.cristin.no/v2/results?institution={institution}&per_page=1000")
sys.stdout.write("Working")

rawData = json.loads(thisPage.text)
data = json_normalize(rawData)

while not done:
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
        sys.stdout.write(" Done!")
        print(f"\nThe last page of the API call is: https://api.cristin.no/v2/results?institution=7548&page={counter}&per_page=1000")
        done = True
data.to_excel("Publications.xlsx", index=False)
