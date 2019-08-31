import time
import json
import os
import sys
import urllib.request

sys.path.append('/home/cdp/crawler/project/database')
import database

client_id = "Q9zDgMB2fgsgIjJwdydO"
client_secret = "OB0768UV0Z"

db = database.Database()

def tagReplace(string):
    result = string.replace("<b>","")
    result = result.replace("</b>","")
    result = result.replace("|",",")
    return result

# Get book information
infoF = open('./bookInfo.txt','r')
bookInfo = infoF.read()
info = []
info = bookInfo.split('^')
info.pop()
infoCnt = 0
 
f = open('./bookCommon.txt','r')

while True:
    line = f.readline()
    index = line.find("^")
    name = line[:index]
    href = line[index+1:]
    href = href.replace("\n","")
    if not name:
        db.dbClose()
        break

    print("name:",name)
    if name[-1].isdigit():
        if name[-2].isdigit():
            pass
        else:
            name = name[:-1]  

    encText = urllib.parse.quote(name)
    url = "https://openapi.naver.com/v1/search/book.json?query=" + encText + "&display=20"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        data = json.loads(response_body)

        for i in range(0,20):
            if (str(data['items'][i]['link'])) == (str(href)):
                    #Title
                    data['items'][i]['title'] = tagReplace(data['items'][i]['title'])
                    data['items'][i]['author'] = tagReplace(data['items'][i]['author'])
                    db.dbConnect()
			
                    title = data['items'][i]['title']
                    image = data['items'][i]['image']
                    author = data['items'][i]['author']
                    price = int(data['items'][i]['price'])
                    isbn = data['items'][i]['isbn']
                    pubdate = int(data['items'][i]['pubdate'])

                    db.bookInsert(title, image, author, price, isbn, pubdate, info[infoCnt])

                    time.sleep(1)
                    print("ok")
                    infoCnt = infoCnt + 1
                    break
    else:
        print("Error Code:",rescode)

