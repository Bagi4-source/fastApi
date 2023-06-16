from fastapi import FastAPI, Request, HTTPException
from models import Product, Message, Translation, TranslationPackages
from tools import AP, install, parse_product
import argostranslate.translate

app = FastAPI()


@app.get("/get_product/", response_model=Product,
         responses={
             404: {
                 "model": Message,
                 "description": "The product was not found"
             },
             200: {
                 "description": "Product requested by spuId",
             }
         })
async def get_product(spu: str):
    return await parse_product(spu)


@app.post("/translate", response_model=Translation, responses={
    200: {
        "description": "Translated text",
    }
})
async def translate(text: str, from_code: str, to_code: str):
    if not install(from_code, to_code):
        raise HTTPException(status_code=422, detail="Incorrect codes")

    translation = argostranslate.translate.translate(text, from_code, to_code)

    return {
        "from_code": from_code,
        "to_code": to_code,
        "translation": translation
    }


@app.get("/translate/get_codes", response_model=TranslationPackages)
async def get_translation_codes():
    return [
        {
            'package': x,
            'from_code': x.from_code,
            'to_code': x.to_code
        } for x in AP
    ]
