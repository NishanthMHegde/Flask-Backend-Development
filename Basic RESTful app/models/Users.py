from db import db

class UsersModel(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50))
	password = db.Column(db.String(50))

	def __init__(self, username, password):
		self.username = username
		self.password = password

	@classmethod
	def find_user_by_username(cls, username):
		# connection = sqlite3.connect('data.db')
		# cursor = connection.cursor()
		# query = "SELECT * from users WHERE username=?"
		# result = cursor.execute(query, (username,)) #data to be passed to ? should always be a tuple
		# row = result.fetchone()
		# if row:
		# 	user = cls(row[0], row[1], row[2])
		# 	return user
		# else:
		# 	return None
		# connection.commit()
		# connection.close()
		user = cls.query.filter_by(username=username).first()
		return user

	@classmethod
	def find_user_by_id(cls, id):
		# connection = sqlite3.connect('data.db')
		# cursor = connection.cursor()
		# query = "SELECT * from users WHERE id=?"
		# result = cursor.execute(query, (id,)) #data to be passed to ? should always be a tuple
		# row = result.fetchone()
		# if row:
		# 	user = cls(row[0], row[1], row[2])
		# 	return user
		# else:
		# 	return None
		# connection.commit()
		# connection.close()
		user = cls.query.filter_by(id=id).first()
		return user

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()