from ctypes import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from fastapi import Body
from typing import Union, List

from app.model import (BookNoId, Book)

from app.db import (
     do_query_books,
     insert_book,
     incrSequence,
     do_query_bookID,
     modify_book
 )

import json

#App Object
app = FastAPI()

##############################################
# (1) react server port not needed here
#origins = ['https://localhost:3000']

app.add_middleware( CORSMiddleware, 
                    #allow_origins = origins, --- see comment (1)
                    allow_credentials = True, 
                    allow_methods = ["*"], 
                    allow_headers= ["*"]
                    )
################################################
# not requested in the challenge a root landing page
@app.get("/")
def read_root():

    return {"STX": "Challenge"}

################################################
# challenge 1 - end point
@app.get("/api_spec")
def read_spec():
    #read configuration

    with open("config.json", "r") as rf:
        return json.load(rf)['APP']

################################################
# challenge 2 - list books end point
@app.get("/books", response_model = List[Book])
async def read_book(author: str, 
                    year_from :str = "skip", 
                    year_to :str = "skip", 
                    acquire :str = "skip"):

    print(f'author: {author}')
    response = await do_query_books(authors = author, 
                                    year_from = year_from, 
                                    year_to = year_to, 
                                    acquire_status = acquire)
    
    response_list = []
    async for document in response:
       response_list.append(document)
    return response_list

################################################
# challenge 3 - get book by ID end point
@app.get("/books/{id}", response_model= Book)
async def read_book_byID(id):
    #print(f'Book ID : {id}' )
    response = await do_query_bookID(idx = id)
    #print(f'Book ID : {response}' )
    return response


################################################
# challenge 4 - add book end point
@app.post("/addbooks", response_model = Book)
async def add_book(bknoid: BookNoId):

    num = await incrSequence()
  
    bookID = Book(id = num , external_id = bknoid.e_id, title = bknoid.ttle, authors = bknoid.auth, published_year= bknoid.publ, 
                acquired = bknoid.acq, thumbnail = bknoid.thbnail)
    
    response = await insert_book(bookID)
   
   
    return response
    
################################################
# challenge 5 - update book end point
@app.post("/books/{id}", response_model = Book)
async def modify_book_ID(id, acqure :bool):
    #get book by  ID
    response = await modify_book(idx = id, acquire = acqure)
    return response

    #get acquire

################################################
# challenge 6 - Delete
# not finished by lack of time

################################################
# challenge 7 - Pool book from Google API / Update / Insert
# not finished by lack of time
# a starting point create in file callGoogleApi.py I planned to
# - connect to Google API (the key will expire in 6 days)
# - pool data into a structure BookGoogle then based on this find/update or create entities

################################################
# challenge 8 - Build and deploy
# Choose Google Cloud Run solution (already has something in Google cloud)
# it was something new for me as I never deal with deployment, still: 
# - manage to create a Dockerfile
# - Create a Google project 
# - Fail to (for mistery reason) build container on Google Cloud got an error: "no concurrent builds quotas available"
#   even if in the choosen region europe-west4 (try on west3 also) I can see 10 quotas available" 
# I give up deployment but despite being quite advanced.