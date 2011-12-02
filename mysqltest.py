import MySQLdb
import pprint


conn = MySQLdb.connect('razanw4.razanw.org', 'razanw', 'Mugga25.', 'razanw4')
conn2 = MySQLdb.connect('razanw4.razanw.org', 'razanw', 'Mugga25.', 'alahazrat2011')

c = conn.cursor()
c.execute("SELECT * from xoops_users")

a = c.fetchall()

a = list(a)

pprint.pprint(a)

c2 = conn2.cursor()
c2.executemany(
	"""INSERT INTO xbd9_users VALUES 
	(%s, 
	%s, 
	%s, 
	%s, 
	%s, 
	%s, 
	%s, 
	%s, 
	%s, 
	%s, 
	%s, 
	%s, 
	%s, 
	%s, 
	%s, 
	%s, 
	%s, 
	%s, 
	%s, 
	%s, 
	%s, 
	%s, 
	%s, 
	%s, 
	%s, 
	%s, 
	%s, 
	%s, 
	%s, 
	%s, 
	%s)""", 
	a)
