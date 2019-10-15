"""Flask server"""
from json import dumps
from flask import Flask, request

from utils import is_valid_email

APP = Flask(__name__)

users = None

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

@auth_api.route('/auth/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    raise ValueError if !is_valid_email(email)

    pass

@auth_api.route('/auth/logout', methods=['POST'])
def logout():
    pass

if __name__ == '__main__':
    APP.run()
