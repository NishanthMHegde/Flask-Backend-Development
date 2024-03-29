from db import db 

class StoreModel(db.Model):
	__tablename__ = 'stores'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	items = db.relationship('ItemModel', lazy='dynamic') # lazy=dynamic loads the items via the query.all() only when it is references via self.items

	def __init__(self, name):
		self.name = name

	def json(self):
		return {'name': self.name, 'items': [item.json() for item in self.items.all()]} #self.items.all() will result in the items being obtained from DB via query.all()

	@classmethod
	def find_by_name(cls, name):
		return cls.query.filter_by(name=name).first()

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_store(self):
		db.session.delete(self)
		db.session.commit()