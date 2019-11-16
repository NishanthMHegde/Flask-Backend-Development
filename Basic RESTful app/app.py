from flask import Flask, request
from flask_restful import Resource,Api
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

#create an Item resource
items = []
class Item(Resource):
	"""
	the function names should correspond to the HTTP verbs get, put, post, delete,etc.
	No app.route() decorator is required.

	"""
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
app.run(port=5002, debug=True)