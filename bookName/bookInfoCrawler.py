from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
driver = webdriver.PhantomJS('/usr/local/share/phantomjs/bin/phantomjs')


writeFile = open("./bookInfo.txt", 'w')
bookInfo = []

with open('./bookCommon.txt') as f:
	for line in f:
		index = line.find('^')
		URL = line[index+1:]
		print(line)
		driver.implicitly_wait(3)
		driver.get(URL)

		try:
			html = driver.page_source
			soup = BeautifulSoup(html, 'html.parser')
			openBtn = driver.find_element_by_id('bookIntroOpen')
			openBtn.click()

		except ElementNotVisibleException:
			pass

		intro = driver.find_element_by_id('bookIntroContent')
		writeFile.write(intro.text)
		sleep(1)
		writeFile.write('^')
# check value (empty)
for i in range(len(bookInfo)):
	assert bookInfo[i] != ''

driver.quit()
writeFile.close()
