from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

import time

while True:
	try:
		driver = webdriver.PhantomJS('/usr/local/share/phantomjs/bin/phantomjs')
		driver.set_window_size(1920, 1080) 
		driver.get("https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=196542784")
		time.sleep(3)

		# ---------------------------------------------------------------
		# scroll down to bottom
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
		html = driver.page_source
		soup = BeautifulSoup(html, 'html.parser')

		# Paging
		i = 1
		while True:
			try:
				pageBtn = driver.find_element_by_xpath("//a[@href='javascript:MyReviewMore();']")
				print(pageBtn)
				print("page")
				pageBtn.click()
				print("pageBtn %d" %i)
				i = i+1
				time.sleep(3)
			except NoSuchElementException:
				break
		i=1
		while True:
			try:
				spoiler = driver.find_element_by_class_name("spo")
				print(spoiler)
				#for i in range(0, len(spoiler):
				print("spo")
				spoiler.click()
				print("spoiler %d" %i)
				i=i+1
				time.sleep(1)
			except NoSuchElementException:
				break

		time.sleep(3)

		while True:
			try:
				test = driver.find_elements_by_css_selector("a.Ere_sub_gray8")
				print(test[7].get_attribute['onclick'])
				moreBtn = driver.find_element_by_link_text("+ 더보기")
				print("more")
				print(moreBtn)
				moreBtn.click()
				time.sleep(1)
			except NoSuchElementException:
				break

		review_titles = driver.find_elements_by_css_selector("div.np_myreview > div.np_myreview > div.Ere_prod_mblog_R > div.hundred_list > div.HL_write")
		review_rates_pre = driver.find_elements_by_css_selector("div.np_myreview > div.np_myreview > div.Ere_prod_mblog_R > div.hundred_list > div.HL_star > img")
		review_contents = driver.find_elements_by_css_selector("div.paper-contents") 

		# 5 slice in list
		def chunker(seq, size):
			return (seq[pos:pos + size] for pos in range(0, len(seq), size))

		review_rates = []
		if len(review_rates_pre) > 0:
			for review_rate in chunker(review_rates_pre, 5):
				stars = 0
				for i in range(5):
					star = review_rate[i].get_attribute('src')
					print("star:",star)
					if "icon_star_on" in star:
						stars = stars + 1
					elif "icon_star_off" in star:
						pass
				review_rates.append(stars)

		for i in range(len(review_titles)):
			print("title: ", review_titles[i].text)
			print("rate: ", review_rates[i])
			print(review_contents[i].text)

		if len(review_titles) == 0:
			print("No Review")

		driver.quit()

	except Exception as e:
	    continue
