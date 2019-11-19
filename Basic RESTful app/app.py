from flask import Flask
from flask_restful import Resource,Api
from flask_jwt import JWT
from security import authenticate,identity
from userregister import UserRegister
from item import Item, ItemsList

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
# items = []

#add our resources to our API and also specify the common endpoints for all our HTTP requests
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemsList, '/items')
api.add_resource(UserRegister, '/register')

#run our app only if this app.py file is called as the main function
if __name__ == "__main__":
	app.run(port=5002, debug=True)