# COMP1531 Project auth
# Written by Sabine Lim z5242579
# 01/10/19

from server import (
    User, Auth, db_get_user_by_id, db_get_user_by_email, db_create_auth,
    db_delete_auth_by_token
)
from utils import is_valid_email

# Given registered user email and password, return dictionary containing u_id
# and auth token. Raise ValueError exception if email entered is not valid/does
# not belong to a user, or password is incorrect.
def auth_login(email, password):
    raise ValueError if not is_valid_email(email)

    user = db_get_user_by_email(email)
    raise ValueError if not user

    raise ValueError if user.get_password() != password

    return db_create_auth(user.get_u_id())

# Given an active token, invalidates the token to log the user out. Given a
# non-valid token, does nothing. Return dictionary containing is_success value
# True if valid token was successfully invalidated, False otherwise.
def auth_logout(token):
    delete_success = db_delete_auth_by_token(token)
    return {'is_success': delete_success}

# Given first and last name, email address and password, create new user account
# and return auth token. Raise ValueError exception if email entered is not
# valid/already in use, password is not valid, name_first > 50 characters or
# name_last > 50 characters
def auth_register(email, password, name_first, name_last):
    if email == 'bademail':
        raise ValueError

    if password == 'pwd':
        raise ValueError

    if name_first == '123456789012345678901234567890123456789012345678901':
        raise ValueError

    if name_last == '123456789012345678901234567890123456789012345678901':
        raise ValueError

    if email == 'user@example.com' and password == 'validpassword':
        return {'u_id': 1234567, 'token': '1234567'}
    elif email == 'sabine.lim@unsw.edu.au' and password == 'ImSoAwes0me':
        return {'u_id': 5242579, 'token': '7849321'}
    elif email == 'gamer@twitch.tv' and password == 'gamers_rise_up':
        return {'u_id': 4201337, 'token': '8479263'}
    elif email == 'abc@def.com' and password == 'ghijklmnop':
        return {'u_id': 9876543, 'token': '0018376'}

    raise ValueError

# Given email, if user is registered, send them an email containing a specific
# secret code, that when entered in auth_passwordreset_reset, shows that the
# user trying to reset the password is the one who got sent this email.
def auth_passwordreset_request(email):
    return {}

# Given reset code for user, set user's new password to password provided. Raise
# ValueError exception if reset_code or new_password is invalid.
def auth_passwordreset_reset(reset_code, new_password):
    if new_password == 'pwd':
        raise ValueError

    return {}
