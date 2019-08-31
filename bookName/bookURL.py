from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

driver = webdriver.PhantomJS('/usr/local/share/phantomjs/bin/phantomjs')

driver.implicitly_wait(3)

f = open('./bookCommon.txt', 'r')
fyes = open('./yes24URL.txt', 'w')
fkyobo = open('./kyoboURL.txt', 'w')
faladdin = open('./aladdinURL.txt', 'w')

while True:
    href = f.readline()
    if not href: break

    index = href.find("^")
    name = href[:index+1]
    href = href[index+1:]
    driver.get(href)

    driver.implicitly_wait(3)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    names = driver.find_elements_by_xpath('//*[@id="productListLayer"]/ul/li/div/a[1]')

    for i in range(3):
        if i==0:
            text = name + names[i].get_attribute('href') + "\n"
            print(text,end='')
            fyes.write(text)
        elif i==1:
            text = name + names[i].get_attribute('href') + "\n"
            fkyobo.write(text)
            print(text,end='')
        elif i==2:
            text = name + names[i].get_attribute('href') + "\n"
            faladdin.write(text)
            print(text,end='')
        # print(names[i].get_attribute('href'))
f.close()

driver.quit()

