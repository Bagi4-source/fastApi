from pprint import pprint

import requests

# spu = 'https://dw4.co/t/A/1Gzc1gsi'
spu = '2444035'
r = requests.get('http://194.58.109.219:8000/api/v3/redoc',
                 params={
                     'apikey': 'K9nhzyw1YxrUa2ODuHJoCLbOr8bxHWFR',
                     'spu': spu
                 })
pprint(r.text)
