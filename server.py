"""Flask server"""
import sys
from flask_cors import CORS
from json import dumps
from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from werkzeug.exceptions import HTTPException
from flask_cors import CORS

from backend.auth import (
    auth_login, auth_logout, auth_register, auth_passwordreset_request,
    auth_passwordreset_reset
)
from backend.user import (
    user_profile, user_profile_setname, user_profile_setemail,
    user_profile_sethandle
)
from backend.channels import channels_create, channels_list, channels_listall
from backend.channel import (
    channel_invite, channel_details, channel_join, channel_leave, channel_messages
)
from backend.message import (
    message_sendlater, message_send, message_remove, message_edit,
    message_react, message_unreact, message_pin, message_unpin
)
from backend.admin import admin_userpermission_change
from backend.standup import standup_start, standup_send
from backend.error import default_handler, ValueError, AccessError

APP = Flask(__name__)
APP.config['TRAP_HTTP_EXCEPTIONS'] = True

APP.register_error_handler(Exception, default_handler)
CORS(APP)



@APP.route('/valueerror')
def login():
    raise ValueError(description="Channel name is bad")
@APP.route('/accesserror')
def logout():
    raise AccessError(description="Access name is bad")


########
# Mail #
########

APP.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = '1531yeetbear@gmail.com',
    MAIL_PASSWORD = "bunchofslackrs"
)

def send_mail(recipients, title, body):
    mail = Mail(APP)
    try:
        msg = Message(title, sender="1531yeetbear@gmail.com", recipients=recipients)
        msg.body = body
        mail.send(msg)
        return "Mail sent!"
    except Exception as e:
        return (str(e))

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

@APP.route('/auth/register', methods=['POST'])
def req_auth_register():
    email = request.form.get('email')
    password = request.form.get('password')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')
    return dumps(auth_register(email, password, name_first, name_last))

@APP.route('/auth/passwordreset/request', methods=['POST'])
def req_auth_passwordreset_request():
    email = request.form.get('email')
    content = auth_passwordreset_request(email)
    if content != {}:
        send_mail(content['recipients'], content['title'], content['body'])
    return dumps({})

@APP.route('/auth/passwordreset/reset', methods=['POST'])
def req_auth_passwordreset_reset():
    reset_code = request.form.get('reset_code')
    new_password = request.form.get('new_password')
    return dumps(auth_passwordreset_reset(reset_code, new_password))

##################
# user interface #
##################

@APP.route('/user/profile', methods=['GET'])
def req_user_profile():
    token = request.args.get('token')
    u_id = int(request.args.get('u_id'))
    return dumps(user_profile(token, u_id))

@APP.route('/user/profile/setname', methods=['PUT'])
def req_user_profile_setname():
    token = request.form.get('token')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')
    return dumps(user_profile_setname(token, name_first, name_last))

@APP.route('/user/profile/setemail', methods=['PUT'])
def req_user_profile_setemail():
    token = request.form.get('token')
    email = request.form.get('email')
    return dumps(user_profile_setemail(token, email))

@APP.route('/user/profile/sethandle', methods=['PUT'])
def req_user_profile_sethandle():
    token = request.form.get('token')
    handle_str = request.form.get('handle_str')
    return dumps(user_profile_sethandle(token, handle_str))

######################
# channels interface #
######################

@APP.route('/channels/create', methods=['POST'])
def req_channels_create():
    token = request.form.get('token')
    name = request.form.get('name')
    is_public = request.form.get('is_public')
    return dumps(channels_create(token, name, is_public))

@APP.route('/channels/list', methods=['GET'])
def req_channels_list():
    token = request.args.get('token')
    return dumps(channels_list(token))

@APP.route('/channels/listall', methods=['GET'])
def req_channels_listall():
    token = request.args.get('token')
    return dumps(channels_listall(token))

#####################
# channel interface #
#####################

@APP.route('/channel/invite', methods=['POST'])
def req_channel_invite():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))
    return dumps(channel_invite(token, channel_id, u_id))

@APP.route('/channel/details', methods=['GET'])
def req_channel_details():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    return dumps(channel_details(token, channel_id))

@APP.route('/channel/join', methods=['POST'])
def req_channel_join():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    return dumps(channel_join(token, channel_id))

@APP.route('/channel/leave', methods=['POST'])
def req_channel_leave():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    return dumps(channel_leave(token, channel_id))

@APP.route('/channel/messages', methods=['GET'])
def req_channel_messages():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))
    return dumps(channel_messages(token, channel_id, start))

#####################
# message interface #
#####################

@APP.route('/message/sendlater', methods=['POST'])
def req_message_sendlater():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    message = request.form.get('message')
    time_sent = request.form.get('time_sent')
    return dumps(message_sendlater(token, channel_id, message, time_sent))

@APP.route('/message/send', methods=['POST'])
def req_message_send():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    message = request.form.get('message')
    return dumps(message_send(token, channel_id, message))

@APP.route('/message/remove', methods=['DELETE'])
def req_message_remove():
    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))
    return dumps(message_remove(token, message_id))

@APP.route('/message/edit', methods=['PUT'])
def req_message_edit():
    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))
    message = request.form.get('message')
    return dumps(message_edit(token, message_id, message))

@APP.route('/message/react', methods=['POST'])
def req_message_react():
    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))
    react_id = int(request.form.get('react_id'))
    return dumps(message_react(token, message_id, react_id))

@APP.route('/message/unreact', methods=['POST'])
def req_message_unreact():
    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))
    react_id = int(request.form.get('react_id'))
    return dumps(message_unreact(token, message_id, react_id))

@APP.route('/message/pin', methods=['POST'])
def req_message_pin():
    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))
    return dumps(message_pin(token, message_id))

@APP.route('/message/unpin', methods=['POST'])
def req_message_unpin():
    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))
    return dumps(message_unpin(token, message_id))

###################
# admin interface #
###################

@APP.route('/admin/userpermission/change', methods=['POST'])
def req_admin_userpermission_change():
    token = request.form.get('token')
    u_id = int(request.form.get('u_id'))
    permission_id = int(request.form.get('permission_id'))
    return dumps(admin_userpermission_change(token, u_id, permission_id))

#####################
# standup interface #
#####################

@APP.route('/standup/start', methods=['POST'])
def req_standup_start():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    length = int(request.form.get('length'))
    return dumps(standup_start(token, channel_id, length))

@APP.route('/standup/send', methods=['POST'])
def req_standup_send():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    message = request.form.get('message')
    return dumps(standup_send(token, channel_id, message))

if __name__ == '__main__':
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000), debug=True)
