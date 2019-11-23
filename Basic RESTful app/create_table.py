import sqlite3

#Always run this script first to create a TABLE.Without table, data cannot be popuated. 
connection = sqlite3.connect('data.db')
cursor = connection.cursor()
query = "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(query)
query = "CREATE TABLE IF NOT EXISTS items(id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(query)
connection.commit()
connection.close()