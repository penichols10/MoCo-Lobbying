import requests
import pandas as pd
import os

limit = 1000
offset = 0
code = 200
while code == 200
    endpoint = f'https://data.montgomerycountymd.gov/resource/j879-q5zd.json$limit={limit}$offset={offset}'
    resp = requests.get(endpoint)
    #df = pd.json_normalize(resp.json())
    print(resp. == 200)