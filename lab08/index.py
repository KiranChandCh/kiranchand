#!/usr/bin/env python3

import cgitb
import pymysql

cgitb.enable()

print("Content-Type:text/html; charset=utf-8")
print()
print("Hello World!")

my_con = pymysql.connect(db='example',user='root', passwd='Kiran@123#', host='localhost')
xc=my_con.cursor()
c.execute("TRUNCATE mytable")

#insert data into database

c.execute("INSERT INTO mytable VALUES(1,'ONE')")
c.execute("INSERT INTO mytable VALUES(2,'Two')")
my_con.commit()

c.execute("Select * FROM mytable")
print(c.fetchall())
