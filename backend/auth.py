# COMP1531 Project auth
# Written by Sabine Lim z5242579
# 01/10/19

from time import time
from jwt import encode as jwt_encode, decode as jwt_decode
from jwt.exceptions import InvalidTokenError

from .db import (
    Role, User, Reset_Request, db_get_all_users, db_get_user_by_u_id,
    db_get_user_by_email, db_create_user, db_get_user_by_handle,
    db_create_reset_request, db_get_reset_request_by_reset_code, get_secret
)
from .utils import is_valid_email, random_string
from .error import (
    ValueError, AccessError
)

############################## Generate Token ########################################

# Returns a new token given a users u_id.

def generate_token(u_id):
    secret = get_secret()
    token_bytes = jwt_encode(
        {
            'u_id': u_id,
            'timestamp': time()
        }, secret, algorithm='HS256'
    )
    token = token_bytes.decode('utf-8')
    return token

############################## Validate Token ########################################

# Return user associated with token.
# Raise AccessError exception if token has been invalidated or if token was not
# generated by server.

def validate_token(token):

    # get the jwt payload
    payload = validate_token_getpayload(token)
    
    # gets the users u_id from the payload
    user = db_get_user_by_u_id(payload['u_id'])
    
    # checks for errors
    validate_token_error(user, payload, token)

    return user

# uses the users secret to retrieve the payload
def validate_token_getpayload(token):
    
    secret = get_secret()
    token_bytes = token.encode()
    try:
        payload = jwt_decode(token_bytes, secret, algorithms=['HS256'])
    # token incorrect
    except InvalidTokenError:
        raise AccessError(description = "Token was not generated by server!")

    return payload

# error list
def validate_token_error(user, payload, token):
    
    # Checks to see if the token was invalidated already
    if not user.has_token(token):
        raise AccessError(description = "Token was invalidated!")

############################## Invalidate Token ########################################

# Invalidate a provided token so all future authorisation attempts with token
# fail.
# Raise AccessError exception if token has already been invalidated.

def invalidate_token(token):
    user = validate_token(token)
    user.remove_token(token)
    return True

############################### Auth Login ########################################

# Given registered user email and password, return dictionary containing u_id
# and auth token. Raise ValueError exception if email entered is not valid/does
# not belong to a user, or password is incorrect.

def auth_login(email, password):

    user = db_get_user_by_email(email)
    
    # error check
    auth_login_error(email, password, user)
    
    # the users u_id
    u_id = user.get_u_id()

    # generate a token and add to account
    token = generate_token(u_id)
    user.add_token(token)

    return {'u_id': u_id, 'token': token}

# error list
def auth_login_error(email, password, user):
    
    # if password doesn't match the user
    if not user.password_matches(password):
        raise ValueError(description = "Incorrect password!")

############################## Auth Logout ########################################

# Given an active token, invalidates the token to log the user out. Given a
# non-valid token, does nothing. Return dictionary containing is_success value
# True if valid token was successfully invalidated, False otherwise.

def auth_logout(token):
    is_success = True
    try:
        invalidate_token(token)
    except AccessError:
        is_success = False
    return {'is_success': is_success}

############################## Is Valid Password ########################################

# Return boolean value indicating whether a password is valid.
def is_valid_password(password):
    if len(password) < 6:
        return False
    return True

########################### Get New User Handle ########################################

# Helper function to interact with the DB and get an appropriate handle.
# Returns string of first_name + last_name maxed out at 20 characters.
# Returns random 20 character alphanumeric string if handle already taken.

def get_new_user_handle(name_first, name_last):
    handle = f"{name_first.lower()}{name_last.lower()}"[0:20]
    while (db_get_user_by_handle(handle, error=False) is not None):
        handle = random_string(20)
    return handle

############################## Auth Register ########################################

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

    # error checks
    auth_register_error(email, password, name_first, name_last)
    
    # First user registered is automatically made owner.
    role = Role.member
    if db_get_all_users() == []:
        role = Role.owner

    # Handle is lowercase first + last name by default.
    handle = get_new_user_handle(name_first, name_last)

    user = db_create_user(email, password, name_first, name_last, handle, role)

    # sets up the u_id and token
    u_id, token = auth_register_credentials(user)

    return {'token': token, 'u_id': u_id}

# sets up the users u_id and token
def auth_register_credentials(user):

    u_id = user.get_u_id()
    token = generate_token(u_id)
    user = db_get_user_by_u_id(u_id)
    user.add_token(token)

    return u_id, token

# error list
def auth_register_error(email, password, name_first, name_last):

    # if the email supplied is invalid
    if not is_valid_email(email):
        raise ValueError(description = "Invalid email")
    
    # if the email is already used
    if db_get_user_by_email(email, error=False):
        raise ValueError(description = "Email already in use")
    
    # password is too short
    if len(password) < 6:
        raise ValueError(description = "Password < 6 characters")
    
    # first name is too long
    if len(name_first) < 1 or len(name_first) > 50:
        raise ValueError(description = "First name not between 1 and 50 characters")
    
    # last name is too long
    if len(name_last) < 1 or len(name_last) > 50:
        raise ValueError(description = "Last name not between 1 and 50 characters")

############################## Auth Passwordreset ########################################

# Given email, if user is registered, send them an email containing a specific
# secret code, that when entered in auth_passwordreset_reset, shows that the
# user trying to reset the password is the one who got sent this email.
# Return dictionary containing email recipients, title and body.

def auth_passwordreset_request(email):

    try:
        user = db_get_user_by_email(email)
    except ValueError:
        return {}

    # Set to expire in 5 minutes
    time_expires = time() + 5 * 60
    reset_request = db_create_reset_request(user, time_expires)

    title = "Your password reset code"
    body = f"Your reset code is {reset_request.get_reset_code()} and will expire in 5 minutes."

    return {'recipients': [email], 'title': title, 'body': body}

############################## Auth Passwordreset Reset ########################################

# Given reset code for user, set user's new password to password provided.
# Return empty dictionary.
# Raise ValueError exception if reset_code or new_password is invalid.

def auth_passwordreset_reset(reset_code, new_password):

    # confirms its the correct reset code supplied
    reset_request = db_get_reset_request_by_reset_code(reset_code)
    
    # error checks
    auth_passwordreset_reset_errors(reset_request, new_password)
    
    user = reset_request.get_user()
    reset_request.expire()

    user.set_password(new_password)

    return {}

# error list
def auth_passwordreset_reset_errors(reset_request, new_password):

    if reset_request is None:
        raise ValueError(description="Reset code is invalid!")
    
    if not is_valid_password(new_password):
        raise ValueError(description="New password is invalid!")
