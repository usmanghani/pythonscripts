#!/opt/local/bin/python2.7 python
# encoding: utf-8
"""
datastoretest.py

Created by Usman Ghani on 2011-02-16.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import MySQLdb

def main():
	conn = MySQLdb.Connect(host='127.0.0.1', user='root', passwd='Mugga25.', db='test')
	cursor = conn.cursor()
	cursor.execute('select * from test')
	print(cursor.fetchall())
	pass


if __name__ == '__main__':
	main()

