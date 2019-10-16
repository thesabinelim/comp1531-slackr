"""Flask server"""
from json import dumps
from flask import Flask, request

from auth import auth_login, auth_logout

APP = Flask(__name__)

##############
# users data #
##############

class User:
    def __init__(self, email, password, name_first, name_last, handle):
        self.email = email
        self.password = password
        self.name_first = name_first
        self.name_last = name_last
        self.handle = handle

    def getEmail(self):
        return self.email
    def getPassword(self):
        return self.password
    def getFirstName(self):
        return self.name_first
    def getLastName(self):
        return self.name_last
    def getHandle(self):
        return self.handle

    def setEmail(self, new_email):
        self.email = new_email
    def setPassword(self, new_password):
        self.password = new_password
    def setFirstName(self, new_name_first):
        self.name_first = new_name_first
    def setLastName(self, new_name_last):
        self.name_last = new_name_last
    def setHandle(self, new_handle):
        self.handle = new_handle

users = None
resetUsers()

##################
# echo functions #
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
# auth functions #
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
