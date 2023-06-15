import json
import logging
import random
import time
from pprint import pprint
import requests
from multiprocessing.pool import Pool
import multiprocessing

from pymongo import MongoClient

proxies = [
    'http://vjVP42:E8NG8W@45.145.57.200:10958',
    'http://vjVP42:E8NG8W@45.145.57.203:10751',
    'http://vjVP42:E8NG8W@45.145.57.203:10750',
    'http://vjVP42:E8NG8W@45.145.57.203:10749',
    'http://rvYBV2:ChGe65@45.145.57.203:10748',
    'http://BUMMoB:Rnzftt@91.218.48.6:9996',
    'http://BUMMoB:Rnzftt@91.218.48.6:9996',
    'http://BUMMoB:Rnzftt@91.218.48.6:9996',
    'http://BUMMoB:Rnzftt@91.218.48.6:9996',
    'http://BUMMoB:Rnzftt@91.218.48.6:9996',
    "http://Pw56Vv:8EWPN7@217.29.53.206:10663",
    "http://Pw56Vv:8EWPN7@217.29.53.206:10662",
    "http://Pw56Vv:8EWPN7@217.29.53.206:10661",
    "http://Pw56Vv:8EWPN7@217.29.53.206:10660",
    "http://Pw56Vv:8EWPN7@217.29.53.206:10659",
    "http://Pw56Vv:8EWPN7@217.29.53.206:10658",
    "http://Pw56Vv:8EWPN7@217.29.53.206:10657",
    "http://Pw56Vv:8EWPN7@217.29.53.206:10656",
    "http://Pw56Vv:8EWPN7@217.29.53.206:10655",
    "http://Pw56Vv:8EWPN7@217.29.53.206:10654",
]


class MongoParser:
    def __init__(self, url):
        self.URL = url
        self.mongo_client = MongoClient(self.URL)
        self.db = None
        self.collection = None

    def set_database(self, db_name):
        self.db = self.mongo_client.get_database(db_name)

    def set_collection(self, collection_name):
        self.collection = self.db.get_collection(collection_name)
        # self.collection.create_index([('detail.spuId', 1)], unique=True)

    def get_product(self, spu):
        url = f'https://cdn.dewucdn.com/spucdn-dewu/dewu/commodity/detail/v2/{spu}.json'
        while True:
            proxy = random.choice(proxies)
            try:
                r = requests.get(url, proxies={
                    'http': proxy,
                    'https': proxy
                })
                break
            except:
                pass

        if r.ok:
            data = self.prepared_data(r.json())
            return data

    def prepared_data(self, data):
        data = data.get('data')
        skus = {}
        for item in data.get('skus', []):
            property_id = item.get('properties')[-1].get('propertyValueId')
            skus[property_id] = item.get('skuId')

        for variant in data.get('saleProperties', {}).get('list', []):
            variant['skuId'] = skus.get(variant.get('propertyValueId'))
            variant.pop('showValue')

        description = {}
        for item in data.get('imageAndText', []):
            key = item.get('contentType')
            if key in ['STORY', 'INTRODUCTION']:
                description[key] = item.get('images', [])[0].get('text')
            else:
                description[key] = item.get('images', [])[0].get('url')

        data['detail']['brandLogoUrl'] = data.get('sizeInfo', {}).get('sizeTemplate', {}).get('brandLogoUrl')
        data['detail']['brandList'] = data.get('baseProperties', {}).get('brandList', [])
        data['detail']['STORY'] = description.get('STORY')
        data['detail']['INTRODUCTION'] = description.get('INTRODUCTION')
        data['detail']['SHOW'] = description.get('SHOW')
        data['detail']['DETAIL'] = description.get('DETAIL')
        data['sizeInfo'] = data.get('sizeInfo', {}).get('sizeTemplate', {}).get('list', [])

        for image in data.get('image', {}).get('spuImage', {}).get('images', []):
            images = data.setdefault('images', [])
            images.append(image.get('url'))

        data['variants'] = data.get('saleProperties', {}).get('list', [])

        properties = {}
        for prop in data.get('baseProperties', {}).get('list', []):
            properties[prop.get('key')] = prop.get('value')

        data['detail']['properties'] = properties

        sizeInfos = []
        for item in data.get('sizeInfo', []):
            if item.get('sizeKey') not in ['EU', 'US', 'UK', 'CM']:
                continue
            item.pop('type')
            sizeInfos.append(item)

        target_keys = ['detail', 'sizeInfo', 'images', 'variants']
        keys = list(data.keys())
        for key in keys:
            if key not in target_keys:
                data.pop(key)
        return data

    def add_item(self, spu):
        print('[SPU]:', spu)
        item = self.get_product(spu)
        try:
            if item:
                self.collection.insert_one(item)
        except:
            pass

    def push_item(self, item):
        self.collection.insert_one(item)

    def push_items(self, items):
        def chunks(lst, n):
            for i in range(0, len(lst), n):
                yield lst[i:i + n]

        for part in chunks(items, 1000):
            self.collection.insert_many(part)

    def get_products(self):
        return self.collection.find()

mongo_parser2 = MongoParser(
    'mongodb+srv://dewu_admin:8I7mp77hxuIXMgG9@cluster0.hugo46h.mongodb.net/?retryWrites=true&w=majority')
mongo_parser2.set_database('dewu_shop')
mongo_parser2.set_collection('products')
mongo_parser2.collection.create_index([('detail.spuId', 1)], unique=True)

mongo_parser2.collection.create_index([('detail.brandId', 1), ('detail.categoryId', 1)])
for i in mongo_parser2.get_products():
    print(i)


if __name__ == "__main__":
    pass
    # mongo_parser = MongoParser()
    # mongo_parser.set_database('shop_db')
    # mongo_parser.set_collection('products')
    # with open('data.json', 'r') as f:
    #     data = json.loads(f.read())
    #     data = data.get("items", [])
    #
    # for i in range(100):
    #     spu_ids = data[1000 * i:1000 * (i + 1)]
    #     if not spu_ids:
    #         break
    #     with Pool(multiprocessing.cpu_count() * 5) as pool:
    #         pool.map(add_item, spu_ids)
    #     time.sleep(2)

    # categories = []
    # for i in mongo_parser.collection.find({}, {'detail': {'brandList': 1}}):
    #     category = i.get('detail', {}).get('brandList', [])[0].get('brandId')
    #     if category not in categories:
    #         categories.append(category)
    #
    # print(categories)
