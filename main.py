import re
import requests
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from Mongo import MongoParser
import sys

app = FastAPI()
sys.setrecursionlimit(2000)


def parse_spu(spu):
    if 'https://dw4.co/t' in spu:
        r = requests.get(spu)
        spu = str(r.url)

    if 'spuId' in spu:
        spu = spu.split('spuId=')[-1].split('&')[0]

    return re.sub(r'\D', '', spu)


async def parse_product(spu):
    mongo_parser = MongoParser(
        'mongodb+srv://dewu_admin:8I7mp77hxuIXMgG9@cluster0.hugo46h.mongodb.net/?retryWrites=true&w=majority')
    mongo_parser.set_database('dewu_shop')
    mongo_parser.set_collection('products')

    spu = parse_spu(spu)
    if not spu:
        return {"error": "spuId is empty"}

    parsed = list(mongo_parser.collection.find({"detail.spuId": int(spu)}))
    if not parsed:
        result = mongo_parser.add_item(spu)
        if not result:
            return {"error": "incorrect spuId"}
        return await parse_product(spu)
    parsed[0].pop('_id')
    return {}


@app.get("/get_product/{spu}")
async def get_product(spu: str):
    return await parse_product(spu)
