import sqlite3


connector = sqlite3.connect("BQACAgIAAxkBAAIBCGM9UyRmMOlqbvA8OLWAp1XSisusAAL8GgACxAPpSWq_YYSa3giUKgQ.db")
cursor = connector.cursor()
cursor.execute("SELECT * FROM users")
r = cursor.fetchall()
print(r)