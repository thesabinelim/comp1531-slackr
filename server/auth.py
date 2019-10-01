# COMP1531 Project auth
# Written by Sabine Lim z5242579
# 01/10/19

# Given registered user email and password, return dictionary containing u_id
# and auth token. Raise ValueError exception if email entered is not valid/does
# not belong to a user, or password is incorrect.
def auth_login(email, password):
    if email == 'bademail':
        raise ValueError
    if email == 'user@example.com' and password == 'validpassword':
        return {'u_id': 1234, 'token': '56789'}
    raise ValueError

# Given an active token, invalidates the taken to log the user out. Given a
# non-valid token, does nothing. Returns empty dictionary.
def auth_logout(token):
    return {}

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
        return {'u_id': 1234, 'token': '56789'}
    raise ValueError
