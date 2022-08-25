
import time
import grequests
import pandas as pd
from urllib.parse import urlencode

df = pd.read_csv('Film_Locations_in_San_Francisco.csv')
search_url = "https://nominatim.openstreetmap.org/search.php"

def preprocessAddress(address = ""):
    if pd.isnull(address):
        return None

    result = address.lower().replace(" ", "+").replace('streets', 'st')#.replace("and", ", ")
    return result

def generateCoordinateCsv(row_number = 10):
    urls = list(map(lambda location: "{}?{}".format(search_url, urlencode({
        "q": preprocessAddress(location),
        "limit": 1,
        "format": "jsonv2"
    })), df.head(row_number)['Locations'].values))

    responses = (grequests.get(url) for url in urls)
    result = grequests.map(responses, size = 30)

    return result

def main():
    start = time.time()
    row_number = 10
    # urls = list(map(lambda location: "{}?{}".format(search_url, urlencode({
    #     "q": preprocessAddress(location),
    #     "limit": 1,
    #     "format": "jsonv2"
    # })), df.head(row_number)['Locations'].values))
    # responses = (grequests.get(url) for url in urls)
    # result = grequests.map(responses, size = 30)

    responses = generateCoordinateCsv(row_number)
    print(list(map(lambda res: res.json(), responses)))
    print("{:.2f} seconds - {} records".format((time.time() - start), row_number))

    # print(result)

    # for index, row in df.head(10).iterrows():
    #     if pd.isnull(row['Locations']):
    #         continue
    
    #     parameters = urlencode({
    #         "q": preprocessAddress(row['Locations']),
    #         "limit": 1,
    #         "format": "jsonv2"
    #     })
    #     urls = "{}?{}".format(search_url, parameters)
        
main()