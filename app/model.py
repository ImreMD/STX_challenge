from unittest.util import strclass
from pydantic import BaseModel, validator
from typing import List, Union


##################################
# with more time I could leverage
# Pydantic capabilities to improve
# the models

##################################
# created a Book class with no ID 
# ID will be supplied by a function
# checking a mongoDB counter
# this is to stick to the technical requirement
# where id is a integer (123, 340, 666)
# MongoDB is using its own ObjectID
##################################
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