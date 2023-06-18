from fastapi import FastAPI, Request, HTTPException
from Translator import Translator
from models import Product, Message, Translation, TranslationPackages, TranslationRequest
from tools import parse_product

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
async def translate(o: TranslationRequest):
    # if (o.from_code, o.to_code) not in [(x.from_code, x.to_code) for x in Translator.get_codes()]:
    #     raise HTTPException(status_code=422, detail="Incorrect codes")

    translation = Translator().translate(o.text, o.from_code, o.to_code)
    if translation:
        return translation
    else:
        raise HTTPException(status_code=404, detail="Error")


@app.get("/translate/get_codes", response_model=TranslationPackages)
async def get_translation_codes():
    return [
        {
            'dir': str(x),
            'from_code': x.from_code,
            'to_code': x.to_code
        } for x in Translator.get_codes()
    ]
