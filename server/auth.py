# COMP1531 Project auth
# Written by Sabine Lim z5242579
# 01/10/19

import re

# Given registered user email and password, return dictionary containing u_id
# and auth token. Raise ValueError exception if email entered is not valid/does
# not belong to a user, or password is incorrect.
def auth_login(email, password):
    if email == 'bademail':
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

# Given an active token, invalidates the token to log the user out. Given a
# non-valid token, does nothing. Returns empty dictionary.
def auth_logout(token):
    return {}

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
    if (not re.search(valid_email_regex(), email)):
        raise ValueError
    # Email already in use
    # TODO - Needs to be a placeholder until users implemented
    
    # Password < 6
    if (len(password) < 6):
        raise ValueError
    # name_first not in range
    if (len(name_first) < 1 or len(name_first) > 50):
        raise ValueError
    # name_last not in range
    if (len(name_last) < 1 or len(name_last) > 50):
        raise ValueError

    # Create an account for the users
    # TODO - requires more thought

    # Handle is lowercase first + last name
    handle = name_first.lower() + name_last.lower()

    # If handle already exists, add a number to it
    # TODO - Requires more thought
    
    # Return a token for the user who registered
    return 'placeholdertoken' # TODO - make this token actually real

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

# Helper function to prevent global variable
# Make a regular expression 
# for validating an Email 
def valid_email_regex():
    return r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'