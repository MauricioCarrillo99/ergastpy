import py_erpy2set as erpy
import requests as r
import pandas as pd
import numpy as np
import json 

url='http://ergast.com/api/f1/2020/seasons.json'
db_seasons=pd.DataFrame(r.get(url).json()['MRData']['seasons']['SeasonTable'])

print(db_seasons)

#erpy.unravel_noKey(db_seasons)
