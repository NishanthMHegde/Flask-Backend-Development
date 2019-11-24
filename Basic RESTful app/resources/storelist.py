import sqlite3
from flask_restful import Resource
from models.store import StoreModel

class StoreList(Resource):
	def get(self):
		# items = []
		# connection = sqlite3.connect('data.db')
		# cursor = connection.cursor()
		# query = 'SELECT * FROM items'
		# rows = cursor.execute(query)
		# for row in rows:
		# 	items.append({'name':row[0], 'price': row[1]})
		# return {'items': items}, 200
		stores = {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}
		return stores