
from cmath import nan
import time
from urllib import response
import grequests
import pandas as pd
import numpy as np
from urllib.parse import urlencode

from requests import Response

df = pd.read_csv('Film_Locations_in_San_Francisco.csv')
# df = pd.read_csv('dataset.csv')
search_url = "https://nominatim.openstreetmap.org/search.php"
coor_dataset = 'Coordinates.csv'

coors = ['lat', 'lon']

def preprocessAddress(address = ""):
    if pd.isnull(address):
        return None

    result = address.lower().replace(" ", "+").replace('streets', 'st')#.replace("and", ", ")
    return result

def generateCoordinateCsv(row_number: int):
    term_df = df.head(row_number)
    urls = list(map(lambda location: "{}?{}".format(search_url, urlencode({
        "q": preprocessAddress(location),
        "limit": 1,
        "format": "jsonv2"
    })), term_df['Locations'].values))
    print(*urls, sep='\n')

    unsent_responses = (grequests.get(url) for url in urls)
    responses = grequests.map(unsent_responses, size = 30)

    json_responses = list(map(lambda response: response.json(), responses))

    coor_df = pd.DataFrame(data={
        'Locations': term_df['Locations'].values,
        'Latitude': [js[0]['lat'] if len(js) > 0 and 'content-type' in response.headers and 'application/json' in response.headers['content-type'] else np.nan for js in json_responses],
        'Longitude': [js[0]['lon'] if len(js) > 0 and 'content-type' in response.headers and 'application/json' in response.headers['content-type'] else np.nan for js in json_responses],
    })

    # lst = list(map(lambda response: response if len(response) > 0 else np.nan, json_responses))

    # print(coor_df)
    total_df = df.merge(right=coor_df, on='Locations', how='left')

    return total_df

def main():
    start = time.time()
    row_number = 12
    # pd.read_csv('Film_Locations_in_San_Francisco.csv').iloc[:, [1, 2]].copy().head(10).to_csv('dataset.csv', index=False)
    print("STARTED ...")
    processed_df = generateCoordinateCsv(row_number)
    print("END after {:.2f} seconds - {} records".format((time.time() - start), row_number))
    print("Exporting CSV ...")
    processed_df.to_csv(coor_dataset, float_format='%.3f')
    print("Exported {} file".format(coor_dataset))

main()