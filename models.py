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
    sizeInfo: List[Size] | None
    variants: List[Variant] | None


class Message(BaseModel):
    detail: str | None


class TranslationMixin(BaseModel):
    from_code: str
    to_code: str


class Translation(TranslationMixin):
    translation: str


class TranslationRequest(TranslationMixin):
    text: str


class TranslationPackages(TranslationMixin):
    dir: str

    def __str__(self):
        return self.dir


class ClipResponse(BaseModel):
    labels: list
    descriptions: list


class ClipResult(BaseModel):
    similarity: dict
    result: list
    compares: dict
    labels: list
