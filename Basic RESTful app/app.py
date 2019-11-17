from flask import Flask, request
from flask_restful import Resource,Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate,identity

app = Flask(__name__)
#create a secret key for app for encoding purpose
app.secret_key = "nishanth"

#add our app to our API
api = Api(app)
#add the authenticate and identity methods we created in security. 
"""
this results in looking for an /auth endpoint request which has body like:
{
	"username": "username",
	"password": "password"
}
"""
jwt = JWT(app, authenticate, identity)  
#an items list which is globally accessible
items = []
#create an Item resource 

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
		item = next(filter(lambda x: x['name'] == name, items), None)
		if item:
			return {'item': item}, 200
		return {'message': "Item does not exist"}, 404

	
	def post(self, name):
		"""
		check if item exists. If it exists, return 400 which is bad request
		"""
		
		item = next(filter(lambda x: x['name'] == name, items), None)
		if item:
			return {'message': 'item already exists'}, 400
		#only parse the data after handling possible errors othewise parsing data would be a waste 
		data = Item.parser.parse_args()
		item = {'name': name, 'price': data['price']}
		items.append(item)
		return {'item': item}, 201

	def delete(self, name):
		"""
		Deletes an aleady existing item
		"""
		global items
		item = next(filter(lambda x: x['name'] == name, items), None)
		if not item:
			return {'message': 'item does not exist'}, 400
		 #Refer to the global items list instead of creating a local variable
		items = list(filter(lambda x: x['name'] != name, items))
		return {'items': items}, 201

	def put(self, name):
		"""
		Check if an item exists. If it exists, then modify it, otherwise create a new one.
		"""
		data = Item.parser.parse_args()
		item = next(filter(lambda x: x['name'] == name, items), None)
		if not item:
			new_item = {'name': name, 'price': data['price']}
			items.append(new_item)
			return {'item': new_item}, 201
		item.update(data)
		return {'item': item}, 201



class ItemsList(Resource):
	def get(self):
		return {'items': items}

#add our resources to our API and also specify the common endpoints for all our HTTP requests
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemsList, '/items')

#run our app
app.run(port=5002, debug=True)