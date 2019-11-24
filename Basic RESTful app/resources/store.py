from models.store import StoreModel
from flask_restful import Resource, reqparse

class Store(Resource):
	def get(self, name):
		store = StoreModel.find_by_name(name)
		if store:
			return store.json(), 200
		return {'message': 'Store with given name could not be found'}, 404
		

	def post(self, name):
		store = StoreModel.find_by_name(name)
		if store:
			return {'message': 'Store with given name already exists'}, 400
		try:
			store = StoreModel(name)
			store.save_to_db()
			return {'message': 'Store was created successfully'}
		except:
			return {'message': 'Store could not be created'}, 500
		
	def delete(self, name):
		store = StoreModel.find_by_name(name)
		if not store:
			return {'message': 'Store with given name could not be found'}, 400
		try:
			store.delete_store()
		except:
			return {'message': 'Store with given name could not be deleted'}, 500
		return {'message': 'Store with given name was deleted'}, 201
