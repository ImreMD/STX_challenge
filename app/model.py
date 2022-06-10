from unittest.util import strclass
from pydantic import BaseModel, validator
from typing import List, Union
from bson.objectid import ObjectId
import asyncio


class BookNoId(BaseModel):
    #id :int -- missing to bypass mongoDB ID_ auto-generation
    e_id :Union [str, None]
    ttle :Union [str, None]
    auth :Union[List[str], List[None]]
    publ :Union [str, None]
    acq :Union [str, bool]
    thbnail :Union [str, None]

    # @validator('acq')
    # def acquired_validator(cls, v):
    #     if v != "skip":
    #         convert_to_bool = (v.lower() == 'true')
    #         return convert_to_bool
    #     else:
    #         return v

class Book(BaseModel):
    id :int
    external_id :Union [str, None]
    title :Union [str, None]
    authors :Union[List[str], List[None]]
    published_year :Union [str, None]
    acquired :Union [str, bool]
    thumbnail :Union [str, None]