import sqlite3
from flask_restful import Resource

class ItemsList(Resource):
	def get(self):
		items = []
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		query = 'SELECT * FROM items'
		rows = cursor.execute(query)
		for row in rows:
			items.append({'name':row[0], 'price': row[1]})
		return {'items': items}, 200