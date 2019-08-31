from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

driver = webdriver.PhantomJS('/usr/local/share/phantomjs/bin/phantomjs')

driver.implicitly_wait(3)
driver.get("https://book.naver.com/bestsell/bestseller_list.nhn?cp=yes24")

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

f = open("./yes24BS.txt", 'w')

for i in range(25):
    i = str(i)
    parse = soup.select('#book_title_'+i+' > a')
    parse = str(parse)

    indexStart = parse.find('href') + 6
    indexLast = parse.find('"', indexStart)
   
    href = parse[indexStart:indexLast]

    indexStart = parse.find('>')
    indexLast = parse.find('<', indexStart)

    name = parse[indexStart+1:indexLast]

    f.write(name+"^"+href+"\n")

f.close()

driver.quit()

