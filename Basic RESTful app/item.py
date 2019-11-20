import sqlite3
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
class Item(Resource):
	"""
	the function names should correspond to the HTTP verbs get, put, post, delete,etc.
	No app.route() decorator is required.

	"""

	#create a parser for parsing JSON arguments to make the price key compulsory for POST/PUT
	#we expect only price from the JSON as name is taken from the endpoint
	parser = reqparse.RequestParser()
	parser.add_argument('price',
		type = float,
		required = True,
		help = 'Price of the item in dollars'
		)

	@jwt_required() #this makes it compulsory to use jwt token in Authorization header
	def get(self, name):
		# item = next(filter(lambda x: x['name'] == name, items), None)
		item = Item.find_by_name(name)
		if item:
			return {'name': item[0], 'price': item[1]}, 200
		return {'message': "Item does not exist"}, 404

	@classmethod
	def find_by_name(cls, name):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		query = "SELECT * FROM items WHERE name=?"
		result = cursor.execute(query, (name,))
		row = result.fetchone()
		connection.commit()
		connection.close()
		return row

	@classmethod
	def insert_item(cls, name):
		data = Item.parser.parse_args()
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		query = "INSERT INTO items VALUES(?,?)"
		result = cursor.execute(query, (name, data['price']))
		connection.commit()
		connection.close()


	def post(self, name):
		"""
		check if item exists. If it exists, return 400 which is bad request
		"""
		
		# item = next(filter(lambda x: x['name'] == name, items), None)
		# if item:
		# 	return {'message': 'item already exists'}, 400
		# #only parse the data after handling possible errors othewise parsing data would be a waste 
		# data = Item.parser.parse_args()
		# item = {'name': name, 'price': data['price']}
		# items.append(item)
		item = Item.find_by_name(name)
		if item:
			return {'message': 'An item with the given name already exists in the database'}
		#only parse the data after handling possible errors othewise parsing data would be a waste
		try:
			self.insert_item(name)
		except:
			return {'message': 'An error occurred during the adding of a new item'}, 500
		return {'message': 'Item was created successfully'}, 201

	def delete(self, name):
		"""
		Deletes an aleady existing item
		"""
		# global items
		# item = next(filter(lambda x: x['name'] == name, items), None)
		# if not item:
		# 	return {'message': 'item does not exist'}, 400
		#  #Refer to the global items list instead of creating a local variable
		# items = list(filter(lambda x: x['name'] != name, items))
		item = Item.find_by_name(name)
		if not item:
			return {'message': 'The item requested cannot be deleted as it does not exist'}, 400
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		query = 'DELETE FROM items WHERE name=?'
		cursor.execute(query, (name,))
		connection.commit()
		connection.close()
		return {'message': 'Item was deleted successfully'}, 201

	def put(self, name):
		"""
		Check if an item exists. If it exists, then modify it, otherwise create a new one.
		"""
		# data = Item.parser.parse_args()
		# item = next(filter(lambda x: x['name'] == name, items), None)
		# if not item:
		# 	new_item = {'name': name, 'price': data['price']}
		# 	items.append(new_item)
		# 	return {'item': new_item}, 201
		# item.update(data)
		# return {'item': item}, 201
		item = Item.find_by_name(name)
		if not item:
			try:
				self.insert_item(name)
				return {'message': 'Item was added successfully'}
			except:
				return {'message': 'An error occurred during the adding of a new item'}, 500
		data = Item.parser.parse_args()
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		query = 'UPDATE items SET price=? WHERE name=?'
		cursor.execute(query, (data['price'], name))
		connection.commit()
		connection.close()
		return {'message': 'Item was modified successfully'}

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