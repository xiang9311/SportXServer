import pymysql  
USER = 'root'
PASSWORD= ''
DATABASE = 'test'
HOST = 'localhost'
#	print('yes')
def get_connection_cur():
	conn = pymysql.connect(host=HOST, port=3306,user=USER,passwd = PASSWORD,db=DATABASE)
	cur=conn.cursor()
	return cur

def close_db(cur):
	cur.close()

def select(DATABASE):
	cur = get_connection_cur()
	cur.execute("select * from qq")
	for r in cur:
		print(r)
	close_db(cur)
def select(DATABASE):
	cur = get_connection_cur()
	cur.execute("select * from %s",DATABASE)
	for r in cur:
		print(r)
	close_db(cur)
select('qq')