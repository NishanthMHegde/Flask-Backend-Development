from db import db

class ItemModel(db.Model):
	__tablename__ = 'items'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	price = db.Column(db.Float(precision=2))
	store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
	stores = db.relationship('StoreModel')

	def __init__(self, name, price, store_id):
		self.name = name
		self.price = price
		self.store_id = store_id

	def json(self):
		return {'name':self.name, 'price': self.price, 'store_id': self.store_id}

	@classmethod
	def find_by_name(cls, name):
		# connection = sqlite3.connect('data.db')
		# cursor = connection.cursor()
		# query = "SELECT * FROM items WHERE name=?"
		# result = cursor.execute(query, (name,))
		# row = result.fetchone()
		# connection.commit()
		# connection.close()
		# if row:
		# 	item = cls(*row) #send the row list as * and constructor will unpack it
		# 	return item
		# return row
		item = cls.query.filter_by(name=name).first() #same as SELECT * FROM items LIMIT 1;
		return item
	
	# def insert_item(self):
	# 	connection = sqlite3.connect('data.db')
	# 	cursor = connection.cursor()
	# 	query = "INSERT INTO items VALUES(?,?)"
	# 	result = cursor.execute(query, (self.name, self.price))
	# 	connection.commit()
	# 	connection.close()

	
	# def update_item(self):
	# 	connection = sqlite3.connect('data.db')
	# 	cursor = connection.cursor()
	# 	query = 'UPDATE items SET price=? WHERE name=?'
	# 	cursor.execute(query, (self.price, self.name))
	# 	connection.commit()
	# 	connection.close()
	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_item(self):
		# connection = sqlite3.connect('data.db')
		# cursor = connection.cursor()
		# query = 'DELETE FROM items WHERE name=?'
		# cursor.execute(query, (self.name,))
		# connection.commit()
		# connection.close()
		db.session.delete(self)
		db.session.commit()
