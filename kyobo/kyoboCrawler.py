from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import sys
import time
import shutil

driver = webdriver.PhantomJS('/usr/local/share/phantomjs/bin/phantomjs')

# for import database module
sys.path.append('/home/cdp/crawler/project/database')         
import database

db = database.Database()
db.dbConnect()

# copy URL file
src = '/home/cdp/crawler/project/bookName/kyoboURL.txt'
dst = '/home/cdp/crawler/project/kyobo/kyoboURL.txt'
shutil.copy(src, dst)

with open('./kyoboURL.txt') as f:
	for line in f:
		index = line.find('^')
		bookTitle = line[:index]
		URL = line[index+1:]
		print(bookTitle, URL)
		driver.get(URL)
		driver.implicitly_wait(3)

		time.sleep(3)

		html = driver.page_source
		soup = BeautifulSoup(html, 'html.parser')

		# Switch popup
		try:
			reviewTab = driver.find_element_by_link_text('전체보기')
			reviewTab.click()

			window_after = driver.window_handles[1]
			driver.switch_to.window(window_after)
			# ------------------------------------------------------

			html = driver.page_source
			soup = BeautifulSoup(html, 'html.parser')

			# Page count
			try:
				page_count = 0
				pages = driver.find_elements_by_css_selector("div.list_paging li")
				for num in pages:
					page_count = page_count + 1
				page_count = page_count / 2 # UP & DOWN
				page_count = int(page_count)

			except NoSuchElementException:
				pass
			# ------------------------------------------------------

			# Review crawling
			for page in range(0, page_count):
			    # Last page
				if page == page_count:
					pass
			    
			    # Remain page
				elif page > 0:
					paging = driver.find_element_by_css_selector("a.btn_next")
					paging.click()
					time.sleep(3)
					html = driver.page_source
					soup = BeautifulSoup(html, 'html.parser')
				    
			    # First page
				else: 
					pass

			    # Crawling
				review_titles = driver.find_elements_by_css_selector("div.title > a > strong")
				review_contents = driver.find_elements_by_css_selector("div.content")
				review_ids = driver.find_elements_by_css_selector("span.info > a")
				review_before_rates = soup.select('body > div > ul > li > div.title > span > img')
			    # Review rate parsing
				review_rates = []
				for i in range(0,len(review_before_rates)):
					parsing_rate = review_before_rates[i].get('alt')
					findIndex = parsing_rate.find('만점에 ')
				
					if(findIndex == -1):
						continue
				
					else:
						parsing_rate = parsing_rate[findIndex+4:findIndex+5]
						review_rates.append(parsing_rate)

			    # Print
				for index in range(0, len(review_titles)):
					db.reviewInsert(bookTitle,review_titles[index].text,review_ids[index].text,review_rates[index],review_contents[index].text,'kyobo')

		except NoSuchElementException:
			print("No Review")

driver.quit()

