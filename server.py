"""Flask server"""
import sys
import os
from flask_cors import CORS
from json import dumps
from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException
from flask_cors import CORS

from backend.auth import auth_login, auth_logout, auth_register
from backend.channels import channels_create
from backend.utils import random_string

from backend.db import db_get_user_by_email

APP = Flask(__name__)
APP.config['TRAP_HTTP_EXCEPTIONS'] = True


##################
# Error Handling #
##################

# As recommended by the course, error handling will be handled similarly to
# https://gitlab.cse.unsw.edu.au/COMP1531/19T3-lectures/blob/master/helper/myexcept.py
def default_handler(err):
    response = err.get_response()
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description()
    })
    response.content_type = 'application/json'
    return response

APP.register_error_handler(Exception, default_handler)
CORS(APP)

class ValueError(HTTPException):
    code = 400
    message = "No message specified"

############
# Database #
############

def get_salt():
    global salt
    return salt

def reset_salt():
    global salt
    salt = os.urandom(32)

salt = None
reset_salt()

def get_secret():
    global secret
    return secret

def reset_secret():
    global secret
    secret = random_string(128)

secret = None
reset_secret()

def get_data():
    global data
    return data

def reset_data():
    global data
    data = {
        'users': [],
        'channels': []
    }

data = None
reset_data()

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

@APP.route('/auth/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    return dumps(auth_login(email, password))

@APP.route('/auth/logout', methods=['POST'])
def logout():
    token = request.form.get('token')
    return dumps(auth_logout(token))

<<<<<<< HEAD
@APP.route('auth/register', methods=['POST'])
def req_auth_register():
    email = request.form.get('email')
    password = request.form.get('password')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')

    token = auth_register(email, password, name_first, name_last)
    u_id = db_get_user_by_email(email).get_user_id()

    return dumps({
        'u_id': u_id,
        'token': token
    })


=======
######################
# channels interface #
######################

@APP.route('channels/create', methods=['POST'])
def create_channel():
    token = request.form.get('token')
    name = request.form.get('name')
    is_public = request.form.get('is_public')
    return dumps(channels_create(token, name, is_public))
>>>>>>> master

if __name__ == '__main__':
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))
