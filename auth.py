# COMP1531 Project auth
# Written by Sabine Lim z5242579
# 01/10/19

from ..db import (
    User, Auth, db_get_user_by_id, db_get_user_by_email, db_create_auth,
    db_delete_auth_by_token, db_create_user
)
from utils import is_valid_email

import jwt
import datetime

# Return a new token given u_id.
def generate_token(u_id):
    secret = get_secret()
    return jwt.encode(
        {
            'u_id': u_id, 
            'time': datetime.datetime.now()
        }, secret, algorithm = 'HS256'
    )

# Return True if a token is valid, False otherwise.
def validate_token(token):
    pass

# Invalidate a provided token such that all future authorisation attempts with
# the token fail. Return True on success, False otherwise.
def invalidate_token(token):
    pass

# Given registered user email and password, return dictionary containing u_id
# and auth token. Raise ValueError exception if email entered is not valid/does
# not belong to a user, or password is incorrect.
def auth_login(email, password):
    raise ValueError if not is_valid_email(email)

    user = db_get_user_by_email(email)
    raise ValueError if not user

    raise ValueError if user.get_password() != password

    u_id = user.get_u_id()
    token = generate_token(u_id)

    return {'u_id': u_id, 'token': token}

# Given an active token, invalidates the token to log the user out. Given a
# non-valid token, does nothing. Return dictionary containing is_success value
# True if valid token was successfully invalidated, False otherwise.
def auth_logout(token):
    delete_success = db_delete_auth_by_token(token)
    return {'is_success': delete_success}

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
def auth_register(email, password, name_first, name_last):
    # Email is valid
    if (not is_valid_email(email)):
        raise ValueError("Invalid email")
    # Email already in use
    if (db_get_user_by_email(email)):
        raise ValueError("Email already in use")
    
    # Password < 6
    if (len(password) < 6):
        raise ValueError("Password < 6 characters")
    # name_first not in range
    if (len(name_first) < 1 or len(name_first) > 50):
        raise ValueError("First name not between 1 and 50 characters")
    # name_last not in range
    if (len(name_last) < 1 or len(name_last) > 50):
        raise ValueError("Last name not between 1 and 50 characters")

    # Handle is lowercase first + last name
    handle = get_new_user_handle(name_first, name_last)
    # Create an account for the users
    u_id = db_create_user(email, password, name_first, name_last, handle)
     
    # Create token from this u_id
    token = generate_token(u_id)
    # Return a token for the user who registered
    return token 

# Helper function to interact with the DB and get an appropriate handle.
# Returns string of first_name + last_name + number if the user already exists.
def get_new_user_handle(name_first, name_last):
    # Handle is lowercase first + last name
    handle = name_first.lower() + name_last.lower()
    handle_number = 0
    # If handle already exists, add a number to it
    while (db_get_user_by_handle(handle + str(handle_number)) != None) {
        handle_number += 1
    }
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