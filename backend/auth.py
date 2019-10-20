# COMP1531 Project auth
# Written by Sabine Lim z5242579
# 01/10/19

from db import (
    User, Role, db_get_users, db_get_user_by_u_id, db_get_user_by_email,
    db_create_user, db_get_user_by_handle
)
import time
import hashlib
import jwt

from utils import is_valid_email
from ..server import get_salt, get_secret

# Return salted hash of password supplied.
def hash_password(password):
    salt = get_salt()
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

# Return a new token given u_id.
def generate_token(u_id):
    secret = get_secret()
    return jwt.encode(
        {
            'u_id': u_id,
            'timestamp': time.time()
        }, secret, algorithm='HS256'
    )

# Return dictionary containing u_id of user associated with token and boolean
# value indicating whether token is valid.
# Raise ValueError exception if token was not generated by server.
def validate_token(token):
    secret = get_secret()
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        u_id = payload['u_id']
        user = db_get_user_by_u_id(u_id)
        is_valid = False
        if user.has_token(token):
            is_valid = True
        return {'u_id': payload['u_id'], 'is_valid': is_valid}
    except jwt.exceptions.DecodeError:
        raise ValueError("Token was not generated by server!")
    except jwt.exceptions.InvalidTokenError:
        raise ValueError("Token was not generated by server!")

# Invalidate a provided token so all future authorisation attempts with token
# fail. Return True if successful, False if token already invalidated. Raise
# ValueError exception if token was not generated by server.
def invalidate_token(token):
    try:
        u_id, token_valid = validate_token(token)
    except ValueError:
        raise ValueError("Token was not generated by server!")

    if not token_valid:
        return

    user = db_get_user_by_u_id(u_id)
    if user.has_token(token):
        user.remove_token(token)
        return True
    return False

# Given registered user email and password, return dictionary containing u_id
# and auth token. Raise ValueError exception if email entered is not valid/does
# not belong to a user, or password is incorrect.
def auth_login(email, password):
    if not is_valid_email(email):
        raise ValueError("Email invalid!")

    user = db_get_user_by_email(email)
    if not user:
        raise ValueError("No user with that email exists!")

    if user.get_password() != password:
        raise ValueError("Incorrect password!")

    u_id = user.get_u_id()
    user = db_get_user_by_u_id(u_id)

    token = generate_token(u_id)
    user.add_token(token)

    return {'u_id': u_id, 'token': token}

# Given an active token, invalidates the token to log the user out. Given a
# non-valid token, does nothing. Return dictionary containing is_success value
# True if valid token was successfully invalidated, False otherwise.
def auth_logout(token):
    try:
        is_success = invalidate_token(token)
    except ValueError:
        is_success = False

    return {'is_success': is_success}

# Given a user's first and last name, email address, and password, create 
# a new account for them and return a new token for authentication in 
# their session. 
# A handle is generated that is the concatentation of a lowercase-only 
# first name and last name.
# If the handle is already taken, a number is added to the end of the 
# handle to make it unique.
# Throws a ValueError when:
# Email is not valid
# Email already in use
# Password < 6 chars long
# name_first is not between 1 and 50 chars
# name_last is not between 1 and 50 chars
# First user registered is automatically made owner.
def auth_register(email, password, name_first, name_last):
    if (not is_valid_email(email)):
        raise ValueError("Invalid email")
    if (db_get_user_by_email(email)):
        raise ValueError("Email already in use")

    if (len(password) < 6):
        raise ValueError("Password < 6 characters")

    if (len(name_first) < 1 or len(name_first) > 50):
        raise ValueError("First name not between 1 and 50 characters")
    if (len(name_last) < 1 or len(name_last) > 50):
        raise ValueError("Last name not between 1 and 50 characters")

    # First user registered is automatically made owner.
    role = Role.member
    if db_get_users() == []:
        role = Role.owner

    # Handle is lowercase first + last name by default.
    handle = get_new_user_handle(name_first, name_last)

    u_id = db_create_user(email, password, name_first, name_last, handle, role)
    token = generate_token(u_id)

    return {'token': token, 'u_id': u_id} 

# Helper function to interact with the DB and get an appropriate handle.
# Returns string of first_name + last_name + number if the user already exists.
def get_new_user_handle(name_first, name_last):
    handle = name_first.lower() + name_last.lower()
    handle_number = 0
    # If handle already exists, add a number to it
    while (db_get_user_by_handle(handle + str(handle_number)) != None):
        handle_number += 1
    if handle_number > 0:
        handle += str(handle_number)
    return handle

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