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
#-------------------------------------------------------------

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
		bookNum = URL[URL.rfind('/')+1:]
		bookNum = bookNum[:-1] # remove \n
		print(bookTitle)

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
			# Find end page for review scraping
			page_end = soup.find("a",{"class":"bgYUI end dim"})
			
			if page_end is None:
				page_end = soup.find("a",{"class":"bgYUI end"})
			if "javascript" in str(page_end):
				page_end = 1
			else:
				page_end = page_end.get('href')
				page_index_start = findnth(page_end, '=', 1)
				page_index_end = findnth(page_end, '&', 1)

				page_end = page_end[page_index_start+1:page_index_end]
				page_end = int(page_end)

			print("page_end:",page_end)
			#------------------------------------------------------------
			# Review scraping

			# Paging
			for num in range(1, page_end+1):
				temp = ["http://www.yes24.com/Product/communityModules/GoodsReviewList/",bookNum,"?Sort=1&PageNumber="]
				page = ''.join(temp)
				page = page + str(num)

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
				review_contents = driver.find_elements_by_css_selector("div.reviewInfoGrp > div.reviewInfoBot.origin > div.review_cont")
				review_rates = driver.find_elements_by_css_selector("div.review_etc > span.review_rating > span.rating")
				review_ids = soup.find_all("a", {"class":"lnk_id"})
				
				# Slice rate (only content rate)
				review_rate = []
				review_rate = review_rates[::2]
				review_rates = review_rate
				for i in range(0, len(review_rates)):
					review_rate[i] = review_rates[i].text[2:3]
				review_rates = review_rate			
				# Print review. complete
				for index in range(0, len(review_titles)):
					db.reviewInsert(bookTitle,review_titles[index].text,review_ids[index].text,review_rates[index],review_contents[index].text,'yes24')
			
					print("ok")

db.dbClose()
driver.quit()

