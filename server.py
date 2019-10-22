"""Flask server"""
import sys
import os
from flask_cors import CORS
from json import dumps
from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException
from flask_cors import CORS

from backend.auth import auth_login, auth_logout, auth_register
from backend.user import (
    user_profile, user_profile_setname, user_profile_setemail,
    user_profile_sethandle
)
from backend.channels import channels_create, channels_list, channels_listall
from backend.channel import channel_invite, channel_join, channel_leave
from backend.message import message_sendlater, message_send
from backend.admin import admin_userpermission_change
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
        'channels': [],
        'messages': []
    }

data = None
reset_data()

##################
# echo interface #
##################

@APP.route('/echo/get', methods=['GET'])
def req_echo_get():
    """ Description of function """
    return dumps({'echo' : request.args.get('echo')})

@APP.route('/echo/post', methods=['POST'])
def req_echo_post():
    """ Description of function """
    return dumps({'echo' : request.form.get('echo')})

##################
# auth interface #
##################

@APP.route('/auth/login', methods=['POST'])
def req_auth_login():
    email = request.form.get('email')
    password = request.form.get('password')
    return dumps(auth_login(email, password))

@APP.route('/auth/logout', methods=['POST'])
def req_auth_logout():
    token = request.form.get('token')
    return dumps(auth_logout(token))

@APP.route('auth/register', methods=['POST'])
def req_auth_register():
    email = request.form.get('email')
    password = request.form.get('password')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')
    return dumps(auth_register(email, password, name_first, name_last))

##################
# user interface #
##################

@APP.route('user/profile', methods=['GET'])
def req_user_profile():
    token = request.args.get('token')
    u_id = request.args.get('u_id')
    return dumps(user_profile(token, u_id))

@APP.route('user/profile/setname', methods=['PUT'])
def req_user_profile_setname():
    token = request.form.get('token')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')
    return dumps(user_profile_setname(token, name_first, name_last))

@APP.route('user/profile/setemail', methods=['PUT'])
def req_user_profile_setemail():
    token = request.form.get('token')
    email = request.form.get('email')
    return dumps(user_profile_setemail(token, email))

@APP.route('user/profile/sethandle', methods=['PUT'])
def req_user_profile_sethandle():
    token = request.form.get('token')
    handle_str = request.form.get('handle_str')
    return dumps(user_profile_sethandle(token, handle_str))

######################
# channels interface #
######################

@APP.route('channels/create', methods=['POST'])
def req_channels_create():
    token = request.form.get('token')
    name = request.form.get('name')
    is_public = request.form.get('is_public')
    return dumps(channels_create(token, name, is_public))

@APP.route('channels/list', methods='GET')
def req_channels_list():
    token = request.args.get('token')
    return dumps(channels_list(token))

@APP.route('channels/listall', methods='GET')
def req_channels_listall():
    token = request.args.get('token')
    return dumps(channels_listall(token))

#####################
# channel interface #
#####################

@APP.route('channel/invite', methods='POST')
def req_channel_invite():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')
    return dumps(channel_invite(token, channel_id, u_id))

@APP.route('channel/join', methods='POST')
def req_channel_join():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    return dumps(channel_join(token, channel_id))

@APP.route('channel/leave', methods='POST')
def req_channel_leave():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    return dumps(channel_leave(token, channel_id))

#####################
# message interface #
#####################

@APP.route('message/sendlater', methods='POST')
def req_message_sendlater():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    message = request.form.get('message')
    return dumps(message_sendlater(token, channel_id, message))

@APP.route('message/send', methods='POST')
def req_message_send():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    message = request.form.get('message')
    return dumps(message_send(token, channel_id, message))

###################
# admin interface #
###################

@APP.route('admin/userpermission/change', methods='POST')
def req_admin_userpermission_change():
    token = request.form.get('token')
    u_id = request.form.get('u_id')
    permission_id = request.form.get('permission_id')
    return dumps(admin_userpermission_change(token, u_id, permission_id))

if __name__ == '__main__':
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))
