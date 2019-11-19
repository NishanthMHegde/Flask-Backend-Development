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

	@classmethod
	def find_by_name(cls, name):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		query = "SELECT * FROM users WHERE username=?"
		result = cursor.execute(query, (name,))
		row = result.fetchone()
		return row

	def post(self):
		data = UserRegister.parser.parse_args()
		user = UserRegister.find_by_name(data['username'])
		if user:
			return {'message': 'A user with the given name already exists'}
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		query = "INSERT into users VALUES(NULL, ?, ?)"
		result = cursor.execute(query, (data['username'], data['password']))
		connection.commit()
		connection.close()
		return {'message': 'Successfully created a new user'}
