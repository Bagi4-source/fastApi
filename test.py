import requests

r = requests.get('http://194.58.109.219:8000/web/get_product/1871373')
print(r.json())
print(r.headers)