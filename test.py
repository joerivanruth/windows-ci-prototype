#!/usr/bin/env python3

from os import environ
import pymonetdb

db_name = environ.get('DB_NAME', 'demo')
db_host = environ.get('DB_HOST', 'localhost')
db_port = environ.get('DB_PORT', 50000)

print("Hello, world!")
print(f"Connecting to «{db_name}» on «{db_host}:{db_port}»")

conn = pymonetdb.connect('demo', host='localhost', port=db_port)
cursor = conn.cursor()

cursor.execute("SELECT * FROM environment")
for key, value in cursor.fetchall():
	print(f"{key:>32}  {value}")