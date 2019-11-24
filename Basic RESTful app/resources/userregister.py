import sqlite3
from flask_restful import Resource, reqparse
from models.Users import UsersModel

class UserRegister(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('username',
		type = str,
		required=True,
		help="Please enter the username")
	parser.add_argument('password',
		type = str,
		required=True,
		help="Please enter the password")

	
	def post(self):
		data = UserRegister.parser.parse_args()
		user = UsersModel.find_user_by_username(data['username'])
		if user:
			return {'message': 'A user with the given name already exists'}
		user = UsersModel(data['username'], data['password'])
		user.save_to_db()
		return {'message': 'User was created successfully'}, 201
