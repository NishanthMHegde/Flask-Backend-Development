from flask import Flask, jsonify, request

#initialize the app
app = Flask(__name__)

#From the server's point of view
#GET: Return the requested data to web application
#POST: Get the incoming data from web application and store it

#create API endpoints

#initialize out stores as an array of dictionaries
stores = []
#return all stores
@app.route('/store', methods=['GET'])
def return_all_stores():
	return jsonify({'stores': stores})

#return store with particular name
@app.route('/store/<string:name>', methods=['GET'])
def return_store(name):
	for store in stores:
		if store['name'] == name:
			return jsonify({'store':store})
	return jsonify({'error': 'Store with mentioned name was not found'})

#return items belonging to a store
@app.route('/store/<string:name>/item', methods=['GET'])
def return_items_from_store(name):
	for store in stores:
		if store['name'] == name:
			return jsonify({'items': store['items']})
	return jsonify({'error': 'Store with mentioned name was not found'})

#Get the store data
@app.route('/store', methods=['POST'])
def get_store():
	request_data = request.get_json()
	new_store = {
	'name':request_data['name'],
	'items': []
	}
	stores.append(new_store)
	return jsonify({'stores': stores})

#Get the item for a partocular store
@app.route('/store/<string:name>/item', methods=['POST'])
def get_item_for_store(name):
	request_data = request.get_json()
	for store in stores:
		if store['name'] == name:
			new_item = {
			'name' : request_data['name'],
			'price': request_data['price']
			}
			store['items'].append(new_item)
			return jsonify({'modified_store': store})
	return jsonify({'error': 'Store with mentioned name was not found'})

#Run the app
app.run(host="127.0.0.1", port = 5001)