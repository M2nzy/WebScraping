import pymysql
from PI import *

class Database:
	def __init__(self):
		self.conn = pymysql.connect(host='localhost', user=ID, password=PW, db=DB)
		self.cur = self.conn.cursor()
	def dbConnect(self):
		sql = "use "+DB
		self.cur.execute(sql)

	def bookInsert(self, title, image, author, price, isbn, pubdate, info):
		self.cur.execute("INSERT INTO book (title, image, author, price, isbn, pubdate, info) VALUES (%s,%s,%s,%s,%s,%s,%s)",(title, image, author, price, isbn, pubdate, info))
		self.cur.connection.commit()

	def reviewInsert(self, bookTitle, title, ID, rate, content, source):
		self.cur.execute("INSERT INTO review (bookTitle, title, id, rate, content, source) VALUES (%s,%s,%s,%s,%s,%s)",(bookTitle, title, ID, rate, content, source))
		self.cur.connection.commit()

	def dbClose(self):
		self.cur.close()
		self.conn.close()

