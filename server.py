"""Flask server"""
import sys
import os
from flask_cors import CORS
from json import dumps
from flask import Flask, request

from backend.auth import auth_login, auth_logout
from backend.utils import random_string

APP = Flask(__name__)
CORS(APP)

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

if __name__ == '__main__':
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))
