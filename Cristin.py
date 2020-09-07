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
totalHits = thisPage.headers["X-Total-Count"]

flatData = json_normalize(json.loads(thisPage.text))
cleanData = flatData[["url"]]

while not done:
    nextPage = requests.get(thisPage.links["next"]["url"])
    try:
        if nextPage.links["next"] is not None:
            thisPage = nextPage
            counter = counter + 1
            sys.stdout.flush()
            sys.stdout.write(".")
            flatData = flatData.append(json_normalize(json.loads(thisPage.text)), sort=True)
            cleanData = flatData[["url"]]
    except KeyError:
        flatData = flatData.append(json_normalize(json.loads(nextPage.text)), sort=True)
        cleanData = flatData[["url"]]
        counter = counter + 1
        sys.stdout.write(" Done!")
        done = True

### Check if all data is gathered ###
totalHits = int(totalHits) + 1
if len(cleanData.index) == int(totalHits):
    print("\n=== All data gathered ===")
    
    ### Save to Publications.xlsx ###
    cleanData.to_excel("Publications.xlsx", index=False)
    print("=== Publications.xlsx written ===")
else:
        print("\n### ERROR WHILE FETCHING DATA ###")


