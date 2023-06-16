# from pprint import pprint
#
import requests
#
# # spu = 'https://dw4.co/t/A/1Gzc1gsi'
# spu = '2444035'
# r = requests.get('http://194.58.109.219:8000/api/v3/get_product/',
#                  params={
#                      'apikey': '10eWMOGJ0CbclthTww94NJliujh8G2g6',
#                      'spu': spu
#                  })
# pprint(r.json())

r = requests.post('http://127.0.0.1:8008/translate', json={
    'text': 'hello',
    'from_code': 'en',
    'to_code': 'ru'
})
print(r.json())