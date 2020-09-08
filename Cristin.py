import json
import sys
import requests
import pandas as pd
from pandas.io.json import json_normalize

### Set desired institution ###
institution = 7548

### Send initial API call, fetch, flatten and store first set of data ###
print("Sending initial API call...")
done = False
thisPage = requests.get(f"https://api.cristin.no/v2/results?institution={institution}&per_page=200")
sys.stdout.write("Gathering all relevant data")
totalHits = thisPage.headers["X-Total-Count"]
flatData = json_normalize(json.loads(thisPage.text))
cleanData = flatData[["url"]]

    
### Loop through all relevant pages of API, fetch, flatten, clean and store data ###
while not done:
    nextPage = requests.get(thisPage.links["next"]["url"])
    try:
        if nextPage.links["next"] is not None:
            thisPage = nextPage
            sys.stdout.flush()
            sys.stdout.write(".")
            flatData = flatData.append(json_normalize(json.loads(thisPage.text)), sort=True)
            cleanData = flatData[["url"]]
    except KeyError:
        flatData = flatData.append(json_normalize(json.loads(nextPage.text)), sort=True)
        cleanData = flatData[["url"]]
        sys.stdout.write(" Done!")
        done = True

### Check if all data is gathered ###
if len(cleanData.index) == int(totalHits):
    print("\n=== All data gathered ===")
    
    ### Write to ResultURLs.xlsx ###
    cleanData.to_excel("ResultURLs.xlsx", index=False)
    print("=== Writing ResultURLs.xlsx ===")
    print("=== ResultURLs.xlsx complete ===")

    ### Write all publication details to Publications.xlsx ###
    flatDetails = pd.DataFrame()
    print("=== Writing Publications.xlsx ===")
    for index,url in enumerate(cleanData["url"]):
        print(f'{index} of {totalHits} publications written\r', end="")
        details = requests.get(str(url))
        flatDetails = flatDetails.append(json_normalize(json.loads(details.text)), sort=True)
    print(f'\r{totalHits} of {totalHits} written', end="")
    flatDetails.to_excel("Publications.xlsx", index=False)
    print("=== Publications.xlsx complete ===")
else:
    print("\n### ERROR WHILE FETCHING DATA ###")
    print("### NO DATA WRITTEN TO FILE ###")


