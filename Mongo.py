import logging

import certifi
from pymongo import MongoClient
import requests


class MongoParser:
    def __init__(self, url):
        self.URL = url
        self.mongo_client = MongoClient(self.URL, tlsCAFile=certifi.where())
        self.db = None
        self.collection = None

    def set_database(self, db_name):
        self.db = self.mongo_client.get_database(db_name)

    def set_collection(self, collection_name):
        self.collection = self.db.get_collection(collection_name)
        # self.collection.create_index([('detail.spuId', 1)], unique=True)

    def parse_product(self, spu):
        url = f'https://cdn.dewucdn.com/spucdn-dewu/dewu/commodity/detail/v2/{spu}.json'
        while True:
            try:
                r = requests.get(url)
                break
            except Exception as e:
                logging.error(e)

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
        item = self.parse_product(spu)
        try:
            if item:
                self.collection.insert_one(item)
            else:
                return False
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
