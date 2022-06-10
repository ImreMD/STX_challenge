import requests
import json

################################################
# first steps to build the logic for pulling data 
# from Google API and then update or insert
API_KEY = ""
with open('..\config.json', 'r') as rf:
    API_KEY = json.load(rf)['API_KEY']['GoogleBookAPI']
    
# split list allow to query for multiple authors not only one
authors=','.join(["Kenneth Sisam", "J. R. R. Tolkien"])
URL="https://www.googleapis.com/books/v1/volumes?q=""+inauthor:" + authors +"&key=" + API_KEY
resp = requests.get(URL)
books = resp.json()
books['items'][0]
#id:-----------------------------------------['id']
books['items'][0]['volumeInfo']
#title-------------------------------['title']
#authors---------------------------['authors']
#acquired--------------------------------False
#published_date:-------------['publishedDate']
#thumbnails--------['imageLinks']['thumbnail']