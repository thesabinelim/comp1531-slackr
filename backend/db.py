# COMP1531 Project db
# Written by Sabine Lim z5242579
# 17/10/19

from ..server import get_data, get_salt, get_secret

import hashlib

# Return salted hash of password supplied.
def hash_password(password):
    salt = get_salt()
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

##############
# users data #
##############

class User:
    def __init__(self, u_id, email, hashpass, name_first, name_last, handle):
        self.u_id = u_id
        self.email = email
        self.hashpass = hashpass
        self.name_first = name_first
        self.name_last = name_last
        self.handle = handle

    def get_u_id(self):
        return self.id
    def get_email(self):
        return self.email
    def get_hashpass(self):
        return self.hashpass
    def get_first_name(self):
        return self.name_first
    def get_last_name(self):
        return self.name_last
    def get_handle(self):
        return self.handle

    def set_email(self, new_email):
        self.email = new_email
    def set_hashpass(self, new_hashpass):
        self.hashpass = new_hashpass
    def set_first_name(self, new_name_first):
        self.name_first = new_name_first
    def set_last_name(self, new_name_last):
        self.name_last = new_name_last
    def set_handle(self, new_handle):
        self.handle = new_handle

# Create User with provided details and add to database, return u_id.
def db_create_user(email, password, name_first, name_last, handle):
    db = get_data()
    salt = get_salt()

    u_id = db['users'][-1].get_u_id() + 1
    hashpass = hash_password(password)

    user = User(u_id, email, hashpass, name_first, name_last, handle)
    db['users'].append(user)

    return u_id

# Return User with u_id if they exist in database, None otherwise.
def db_get_user_by_u_id(u_id):
    db = get_data()

    for user in db['users']:
        return user if user.get_u_id() == u_id
    return None

# Return User with handle if they exist in database, None otherwise.
def db_get_user_by_handle(handle):
    db = get_data()

    for user in db['users']:
        return user if user.get_handle() == handle
    return None

# Return User with email if they exist in database, None otherwise.
def db_get_user_by_email(email):
    db = get_data()

    for user in db['users']:
        return user if user.get_email() == handle

# Set User with id's details in database to provided details.
def db_set_user_details(u_id, email, password, name_first, name_last, handle):
    user = db_get_user_by_id(u_id)
    salt = get_salt()

    hashpass = hash_password(password)
    if user:
        user.set_email(email)
        user.set_password(hashpass)
        user.set_first_name(name_first)
        user.set_last_name(name_last)
        user.set_handle(handle)
