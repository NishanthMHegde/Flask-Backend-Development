import sqlite3
from flask_restful import Resource, reqparse

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
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		query = "INSERT into users VALUES(NULL, ?, ?)"
		result = cursor.execute(query, (data['username'], data['password']))
		connection.commit()
		connection.close()
		return {'message': 'Successfully created a new user'}
