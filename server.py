"""Flask server"""
from json import dumps
from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException
from flask_cors import CORS

from backend.auth import auth_login, auth_logout, auth_register
from backend.utils import random_string

from backend.db import db_get_user_by_email

import os

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
        'auths': []
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

@auth_api.route('/auth/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    return dumps(auth_login(email, password))

@auth_api.route('/auth/logout', methods=['POST'])
def logout():
    token = request.form.get('token')
    return dumps(auth_logout(token))

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



if __name__ == '__main__':
    APP.run()