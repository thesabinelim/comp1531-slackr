"""Flask server"""
from json import dumps
from flask import Flask, request

from auth import auth_login, auth_logout
from utils import random_string

APP = Flask(__name__)

############
# Database #
############

def get_data():
    global data
    return data

def reset_data():
    global data
    data = {
        'users': [],
        'auths': []
    }

data = None
reset_data()

##############
# users data #
##############

class User:
    def __init__(self, u_id, email, password, name_first, name_last, handle):
        self.u_id = u_id
        self.email = email
        self.password = password
        self.name_first = name_first
        self.name_last = name_last
        self.handle = handle

    def get_u_id(self):
        return self.id
    def get_email(self):
        return self.email
    def get_password(self):
        return self.password
    def get_first_name(self):
        return self.name_first
    def get_last_name(self):
        return self.name_last
    def get_handle(self):
        return self.handle

    def set_email(self, new_email):
        self.email = new_email
    def set_password(self, new_password):
        self.password = new_password
    def set_first_name(self, new_name_first):
        self.name_first = new_name_first
    def set_last_name(self, new_name_last):
        self.name_last = new_name_last
    def set_handle(self, new_handle):
        self.handle = new_handle

# Create User with provided details and add to database, return u_id.
def db_create_user(email, password, name_first, name_last, handle):
    db = get_data()
    u_id = db['users'][-1].get_u_id() + 1
    user = User(u_id, email, password, name_first, name_last, handle)
    db['users'].append(user)
    return u_id

# Return User with u_id if they exist in database, None otherwise.
def db_get_user_by_u_id(u_id):
    db = get_data()
    for user in db['users']:
        return user if user.get_u_id() == u_id
    return None

# Return User with handle if they exist in database, None otherwise.
def db_get_user_by_handle(handle):
    db = get_data()
    for user in db['users']:
        return user if user.get_handle() == handle
    return None

# Return User with email if they exist in database, None otherwise.
def db_get_user_by_email(email):
    db = get_data()
    for user in db['users']:
        return user if user.get_email() == handle

# Set User with id's details in database to provided details.
def db_set_user_details(u_id, email, password, name_first, name_last, handle):
    db = get_data()
    user = db_get_user_by_id(u_id)
    if user:
        user.set_email(email)
        user.set_password(password)
        user.set_first_name(name_first)
        user.set_last_name(name_last)
        user.set_handle(handle)

##############
# auths data #
##############

class Auth:
    def __init__(self, u_id, token):
        self.u_id = u_id
        self.token = token

    def get_u_id(self):
        return self.u_id

    def get_token(self):
        return self.token

# Create Auth with provided u_id and add to database, return token.
def db_create_auth(u_id):
    db = get_data()

    # Generate a new random token
    token = random_string(7)
    while db_get_auth_by_token(token):
        token = random_string(7)

    # Add new Auth to database
    auth = Auth(u_id, token)
    db['auths'].append(auth)

    return token

# Return Auth with provided token if it exists in database, None otherwise.
def db_get_auth_by_token(token):
    db = get_data()
    for auth in db['auths']:
        return auth if auth.get_token() == token
    return None

# Delete Auth with provided token if it exists in database. Return True if
# successfully found and deleted, False otherwise.
def db_delete_auth_by_token(token):
    db = get_data()
    for auth in db['auths']:
        if auth.get_token() == token:
            db['auths'].remove(auth)
            return True
    return False

##################
# echo interface #
##################

@APP.route('/echo/get', methods=['GET'])
def echo1():
    """ Description of function """
    return dumps({
        'echo' : request.args.get('echo'),
    })

@APP.route('/echo/post', methods=['POST'])
def echo2():
    """ Description of function """
    return dumps({
        'echo' : request.form.get('echo'),
    })

##################
# auth interface #
##################

@auth_api.route('/auth/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    return dumps(auth_login(email, password))

@auth_api.route('/auth/logout', methods=['POST'])
def logout():
    token = request.form.get('token')
    return dumps(auth_logout(token))

if __name__ == '__main__':
    APP.run()
