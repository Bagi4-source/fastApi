import re
import requests
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from Mongo import MongoParser

app = FastAPI()

WHITELISTED_IPS = ['194.58.109.219', '127.0.0.1', '172.19.0.1']


def parse_spu(spu):
    if 'https://dw4.co/t' in spu:
        r = requests.get(spu)
        spu = str(r.url)

    if 'spuId' in spu:
        spu = spu.split('spuId=')[-1].split('&')[0]

    return re.sub(r'\D', '', spu)


def get_product(spu):
    mongo_parser = MongoParser(
        'mongodb+srv://dewu_admin:8I7mp77hxuIXMgG9@cluster0.hugo46h.mongodb.net/?retryWrites=true&w=majority')
    mongo_parser.set_database('dewu_shop')
    mongo_parser.set_collection('products')

    spu = parse_spu(spu)
    parsed = list(mongo_parser.collection.find({"detail.spuId": spu}))
    if not parsed:
        result = mongo_parser.add_item(spu)
        if not result:
            return {"error": "incorrect spuId"}
        return get_product(spu)
    parsed[0].pop('_id')
    return parsed[0]


@app.get("/")
async def root(request: Request):
    ip = str(request.client.host)
    if ip not in WHITELISTED_IPS:
        data = {
            'message': f'IP {ip} is not allowed to access this resource.'
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=data)

    # Proceed if IP is allowed
    return {"message": "Hello World"}


@app.get("/get_product/{spu}")
async def say_hello(spu: str):
    return get_product(spu)
