from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import sys
import shutil

#-------------------------------------------------------------
# Find string (n-1) th
def findnth(string, substring, n):
	parts = string.split(substring, n + 1)
	if len(parts) <= n + 1:
		return -1
	return len(string) - len(parts[-1]) - len(substring)

driver = webdriver.PhantomJS('/usr/local/share/phantomjs/bin/phantomjs')

# For import database module
sys.path.append('/home/cdp/crawler/project/database')         
import database

db = database.Database()
db.dbConnect()

# Copy URL file
src = '/home/cdp/crawler/project/bookName/yes24URL.txt'
dst = '/home/cdp/crawler/project/yes24/yes24URL.txt'
shutil.copy(src, dst)

with open('./yes24URL.txt') as f:
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

		# Check has Review
		noReview = soup.find("div", {"class":"gd_noData"})
		noReview = str(noReview)
		if "None" not in noReview:
			print("No Review")

		else:
			print(driver.current_url)
			# Find end page for review scraping
			page_end = driver.find_elements_by_css_selector("div.review_sort > div.review_sortLft > div.yesUI_pagenS > a")
			print(page_end)
			for i in range(len(page_end)):			
				print(page_end)
			if "javascript" in str(page_end):
				page_end = 1
			else:
				page_end = page_end.get('href')
				page_index_start = findnth(page_end, '=', 1)
				page_index_end = findnth(page_end, '&', 1)

				page_end = page_end[page_index_start+1:page_index_end]
				page_end = int(page_end)
			#------------------------------------------------------------
			# Review scraping

			# Paging
			page = soup.find("a", {"class":"num"})
			if "None" in str(page):
				pass
			else:
				page = page.get('href')
				page = "http://www.yes24.com" + page

				page_index_start = findnth(page, '=', 1)
				page_index_end = findnth(page, '&', 1)
				page_front = page[:page_index_start+1]
				page_back = page[page_index_end:]

			for num in range(1, page_end+1):
				if page_end == 1:
					pass
				else:
					page = page_front+str(num)+page_back

					driver.get(page)
					driver.implicitly_wait(3)
					time.sleep(3)

				html = driver.page_source
				soup = BeautifulSoup(html, 'html.parser')
				print(driver.current_url)
				# ---------------------------------------------------------------
				# Scroll down to bottom
				SCROLL_PAUSE_TIME = 1.5

				# Get scroll height
				last_height = driver.execute_script("return document.body.scrollHeight")
				while True:
					driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

					# Wait to load page
					time.sleep(SCROLL_PAUSE_TIME)

					# Calculate new scroll height and compare with last scroll height
					new_height = driver.execute_script("return document.body.scrollHeight")
					if new_height == last_height:
						break
					last_height = new_height

				# ---------------------------------------------------------------
				# Find reviews
				review_titles = driver.find_elements_by_css_selector("span.review_tit > span.txt")
				review_contents = driver.find_elements_by_css_selector("div.reviewInfoBot.origin > div.review_cont")
				review_rates = driver.find_elements_by_css_selector("div.review_etc > span.review_rating > span.rating")
				review_ids = soup.find_all("a", {"class":"lnk_id"})
				
				print(review_contents[0].text)
				# Slice rate (only content rate)
				review_rate = []
				review_rate = review_rates[::2]
				review_rates = review_rate
				for i in range(0, len(review_rates)):
					review_rate[i] = review_rates[i].text[2:3]
				review_rates = review_rate			

			    # Print review. complete
				for index in range(0, len(review_titles)):
					print("title:", review_titles[index].text)
					print("ID:", review_ids[index].text)
					print("rate:", review_rates[index])
					print("content:", review_contents[index].text, "\n")
			
driver.quit()

