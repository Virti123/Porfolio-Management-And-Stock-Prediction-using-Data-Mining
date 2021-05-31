import MySQLdb

def connection():
	conn = MySQLdb.connect(host="localhost", user="root", db="user")

	c = conn.cursor()

	return c,conn