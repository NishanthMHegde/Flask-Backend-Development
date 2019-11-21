from models.Users import UsersModel
from werkzeug.security import safe_str_cmp

# users = [Users(1, 'nishanth', 'root')]
# user_byusername = {u.username: u for u in users}
# user_byuserid = {u.id: u for u in users}

def authenticate(username, password):
	"""
	This function is used to compare username and password
	ad return the user object if it exists.
	"""
	# user = user_byusername.get(username, None)
	user = UsersModel.find_user_by_username(username)
	if user and safe_str_cmp(user.password, password):
		return user 

def identity(payload):
	"""
	This function is called after authentication is successfu to retrieve the user ID
	"""
	user_id = payload['identity']
	user = UsersModel.find_user_by_id(user_id)
	# user = user_byuserid.get(user_id, None)
	return user 