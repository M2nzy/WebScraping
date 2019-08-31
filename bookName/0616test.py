import time
import json
import os
import sys
import urllib.request

client_id = "Q9zDgMB2fgsgIjJwdydO"
client_secret = "OB0768UV0Z"
name = "윤성우의 열혈 TCP/IP 소켓 프로그래밍"
encText = urllib.parse.quote(name)
url = "https://openapi.naver.com/v1/search/book.json?query=" + encText + "&display=1"
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    data = json.loads(response_body)
        
    for i in range(data['display']):
                #Title
            print(data['items'][i]['title'])
            print(data['items'][i]['image'])
            print(data['items'][i]['author'])
            print(data['items'][i]['price'])
            print(data['items'][i]['isbn'])
            print(data['items'][i]['pubdate'])
            time.sleep(1)
            print("")
            break
    else:
        print("Error Code:" + rescode)
