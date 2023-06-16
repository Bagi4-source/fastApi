import logging
from fastapi import HTTPException
import argostranslate.package
import argostranslate.translate
from Mongo import MongoParser
import requests
import re

AP = argostranslate.package.get_available_packages()
available_packages = [(x.from_code, x.to_code) for x in AP]


def install(from_code, to_code):
    if (from_code, to_code) not in available_packages:
        return
    installed_packages = [(x.from_code, x.to_code) for x in argostranslate.package.get_installed_packages()]
    if (from_code, to_code) not in installed_packages:
        try:
            package_to_install = next(
                filter(
                    lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
                )
            )
            argostranslate.package.install_from_path(package_to_install.download())
        except Exception as e:
            logging.error(f'[INSTALL]: {e}')
            return
    return True


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
        raise HTTPException(status_code=403, detail="Incorrect data")

    # if spu != new_spu:
    #     return RedirectResponse(f'/get_product/?spu={new_spu}')

    parsed = list(mongo_parser.collection.find({"detail.spuId": int(new_spu)}))
    if not parsed:
        result = mongo_parser.add_item(new_spu)
        if not result:
            raise HTTPException(status_code=404, detail="Product not found")
    parsed[0].pop('_id')
    return parsed[0]
