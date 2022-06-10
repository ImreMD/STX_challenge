import requests
import json
 
authors=','.join(["Kenneth Sisam", "J. R. R. Tolkien"])
URL="https://www.googleapis.com/books/v1/volumes?q=""+inauthor:" + authors +"&key=AIzaSyA8chJyP1HwFK3_Ep-txNyupkThIR7lKDE"
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