from pydantic import BaseModel
from typing import List


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


class Message(BaseModel):
    detail: str


class Translation(BaseModel):
    from_code: str
    to_code: str
    translation: str


class TranslationPackages(BaseModel):
    dir: str
    from_code: str
    to_code: str
