import sqlite3

class UsersModel:
	def __init__(self, id, username, password):
		self.id = id
		self.username = username
		self.password = password

	@classmethod
	def find_user_by_username(cls, username):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		query = "SELECT * from users WHERE username=?"
		result = cursor.execute(query, (username,)) #data to be passed to ? should always be a tuple
		row = result.fetchone()
		if row:
			user = cls(row[0], row[1], row[2])
			return user
		else:
			return None
		connection.commit()
		connection.close()

	@classmethod
	def find_user_by_id(cls, id):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		query = "SELECT * from users WHERE id=?"
		result = cursor.execute(query, (id,)) #data to be passed to ? should always be a tuple
		row = result.fetchone()
		if row:
			user = cls(row[0], row[1], row[2])
			return user
		else:
			return None
		connection.commit()
		connection.close()