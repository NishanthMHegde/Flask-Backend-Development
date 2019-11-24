import sqlite3
from models.item import ItemModel
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
	parser.add_argument('store_id',
		type = int,
		required = True,
		help = 'Store id of the store for which the item belongs to'
		)

	@jwt_required() #this makes it compulsory to use jwt token in Authorization header
	def get(self, name):
		# item = next(filter(lambda x: x['name'] == name, items), None)
		item = ItemModel.find_by_name(name)
		if item:
			return item.json(), 200
		return {'message': "Item does not exist"}, 404
	
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
		item = ItemModel.find_by_name(name)
		if item:
			return {'message': 'An item with the given name already exists in the database'}, 400
		data = Item.parser.parse_args()
		new_item = ItemModel(name, data['price'], data['store_id'])
		#only parse the data after handling possible errors othewise parsing data would be a waste
		try:
			new_item.save_to_db()
		except Exception as e:
			print(e)
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
		item = ItemModel.find_by_name(name)
		if not item:
			return {'message': 'The item requested cannot be deleted as it does not exist'}, 400
		try:
			item.delete_item()
		except:
			return {'message': 'An error occurred during the deletion of item'}, 500
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
		data = Item.parser.parse_args()
		item = ItemModel.find_by_name(name)
		
		if not item:
			try:
				new_item = ItemModel(name, data['price'], data['store_id'])
				new_item.save_to_db()
				return {'message': 'Item was added successfully'}
			except:
				return {'message': 'An error occurred during the adding of a new item'}, 500
		try:
			item.price = data['price']
			item.store_id = data['store_id']
			item.save_to_db()
		except:
			return {'message': 'An error occurred during the item update'}, 500
		return {'message': 'Item was modified successfully'}

