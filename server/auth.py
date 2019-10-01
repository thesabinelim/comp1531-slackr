# COMP1531 Project auth
# Written by Sabine Lim z5242579
# 01/10/19

# Given a registered user email and password, returns dictionary containing u_id
# and login token. Raises ValueError exception email entered is not valid/does
# not belong to a user, or password is incorrect.
def auth_login(email, password) {
    return {'u_id': 1234, 'token': '56789'}
}

# Given an active token, invalidates the taken to log the user out. Given a
# non-valid token, does nothing. Returns empty dictionary.
def auth_logout(token) {
    return {}
}
