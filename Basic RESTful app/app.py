from flask import Flask, request
from flask_restful import Resource,Api

app = Flask(__name__)
#add our app to our API
api = Api(app)

#create an Item resource
items = []
class Item(Resource):
	"""
	the function names should correspond to the HTTP verbs get, put, post, delete,etc.
	No app.route() decorator is required.

	"""
	def get(self, name):
		item = next(filter(lambda x: x['name'] == name, items), None)
		if item:
			return {'item': item}, 200
		return {'message': "Item does not exist"}, 404

	def post(self, name):
		"""
		check if item exists. If it exists, return 400 whicch is bad request
		"""
		item = next(filter(lambda x: x['name'] == name, items), None)
		if item:
			return {'message': 'item already exists'}, 400
		data = request.get_json()
		item = {'name': data['name'], 'price': data['price']}
		items.append(item)
		return {'item': item}, 201


class ItemsList(Resource):
	def get(self):
		return {'items': items}

#add our resources to our API and also specify the common endpoints for all our HTTP requests
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemsList, '/items')

#run our app
app.run(port=5002)