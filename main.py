import re
from typing import List

import requests
from fastapi import FastAPI, Request
from pydantic import BaseModel
from starlette.responses import RedirectResponse

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

    new_spu = parse_spu(spu)
    if not new_spu:
        return {"error": "spuId is empty"}

    # if spu != new_spu:
    #     return RedirectResponse(f'/get_product/?spu={new_spu}')

    parsed = list(mongo_parser.collection.find({"detail.spuId": int(new_spu)}))
    if not parsed:
        result = mongo_parser.add_item(new_spu)
        if not result:
            return {"error": "incorrect spuId"}
    parsed[0].pop('_id')
    return parsed[0]


class Brand(BaseModel):
    brandId: int
    brandName: str


class Detail(BaseModel):
    spuId: int
    categoryId: int
    brandId: int
    authPrice: int
    logoUrl: str
    title: str
    subTitle: str
    desc: str
    sourceName: str
    articleNumber: str
    articleNumbers: list
    sellDate: str
    fitId: int
    brandLogoUrl: str
    brandList: List[Brand]
    STORY: str
    INTRODUCTION: str
    SHOW: str
    DETAIL: str
    properties: dict


class Size(BaseModel):
    sizeKey: str
    sizeValue: str


class Variant(BaseModel):
    propertyId: int
    name: str
    value: str
    propertyValueId: int
    level: int
    customValue: str
    sort: int
    definitionId: int
    skuId: int


class Product(BaseModel):
    detail: Detail
    images: List[str]
    sizeInfo: List[Size]
    variants: List[Variant]


@app.get("/get_product/", response_model=Product)
async def get_product(spu: str):
    return await parse_product(spu)
