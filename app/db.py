from pickletools import int4
from pprint import pprint
import motor.motor_asyncio

import asyncio
import datetime
import pprint
from typing import Union
import copy

import json

fake_books_db = [
            {   "id":123,
                "external_id": "rToaogEACAAJ",
                "title": "Hobbit czyli Tam i z powrotem",
                "authors": [
                            "J. R. R. Tolkien"
                            ],
                "acquired": False,
                "published_year": "2004",
                "thumbnail":
        "http://books.google.com/books/content?id=YyXoAAAACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api"

    },
    {       "id": 340,
            "external_id": "EsiJcusIVD",
            "title": "A Middle English Reader",
            "authors": [
                    "Kenneth Sisam",
                    "J. R. R. Tolkien"
                    ],
            "acquired": False,
            "published_year": "2005",
            "thumbnail": None
}

]



#client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://STXNext:challenge@cluster0.toyfu.mongodb.net/?retryWrites=true&w=majority")
db = client.book_db
collection = db.book_collection
counter = db.counter_tracker
counter_init = {"_id" : "bookid", "seq" : 665}

#prepare query depending on number of args
def prepare_query(author, date_f,date_t, acqurd):
      if acqurd != "skip":
            acquired = (acqurd.lower() == 'true')
      else:
            acquired = acqurd

      query = {'year_from': date_f,
               'year_to': date_t,
               'acquired': acquired}
      build_dict = {'authors' : {"$regex": author}}
     
      for key, value in query.items():
            if value == "skip":
                  build_dict
            else:
                  build_dict[key] = value
      build_query={'$and':[build_dict]}
      
      return build_query


async def incrSequence():
     increment =  await counter.update_one({"_id": "bookid"}, { "$inc": {"seq" : 1}}, upsert=True)
     result = await counter.find({"_id":"bookid"}).to_list(1)
     return (result[0]['seq'])


async def init_counter_coll():
      result = await counter.insert_one(counter_init)
      return print(f'counter collection created: {result}')


async def do_first_insert_fake_books():
    
    result = await collection.insert_many(fake_books_db)
    return print(f'insert collection: {result}')

async def do_query_books(authors :str,
                         year_from :str, 
                         year_to :str,
                         acquire_status :str):
  
  query = prepare_query(authors, year_from, year_to, acquire_status)
  print(f'query: {query}')
  cursor = collection.find(query)
  return cursor
  

async def do_query_bookID(idx: int):
       
        query = {"id": int(idx)}
        cursor = await collection.find_one(query)
        return cursor

async def insert_book(book):
    
    document = book.dict()
    
    new_book = await collection.replace_one({"id": document['id']}, document, upsert= True) 
    find_book = await collection.find_one({"$and":[{'authors': document['authors']},
                                                      {'external_id': document['external_id']}]})
    
    return find_book 
  
 
async def modify_book(idx: int, acquire :bool):
      #acqure = (acquire.lower()=='true')
      new_book = await collection.update_one({"id": int(idx)}, {'$set':{'acquired' : acquire}})
      find_book = await collection.find_one({"id": int(idx)})

      return find_book




