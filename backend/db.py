# COMP1531 Project db
# Written by Sabine Lim z5242579
# 17/10/19

from server import get_data, get_salt, get_secret
from auth import hash_password

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
        self.tokens = []

    def get_u_id(self):
        return self.u_id
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
    def get_tokens(self):
        return self.tokens
    def has_token(self, token):
        return token in self.tokens

    def set_email(self, new_email):
        self.email = new_email
    def set_password(self, new_password):
        new_hashpass = hash_password(new_password)
        self.hashpass = new_hashpass
    def set_first_name(self, new_name_first):
        self.name_first = new_name_first
    def set_last_name(self, new_name_last):
        self.name_last = new_name_last
    def set_handle(self, new_handle):
        self.handle = new_handle
    def add_token(self, token):
        self.tokens.append(token)
    def remove_token(self, token):
        self.tokens.remove(token)

# Create User with provided details and add to database, return u_id.
def db_create_user(email, password, name_first, name_last, handle):
    db = get_data()

    u_id = db['users'][-1].get_u_id() + 1
    hashpass = hash_password(password)

    user = User(u_id, email, hashpass, name_first, name_last, handle)
    db['users'].append(user)

    return u_id

# Return User with u_id if they exist in database, None otherwise.
def db_get_user_by_u_id(u_id):
    db = get_data()

    for user in db['users']:
        if user.get_u_id() == u_id:
            return user
    return None

# Return User with handle if they exist in database, None otherwise.
def db_get_user_by_handle(handle):
    db = get_data()

    for user in db['users']:
        if user.get_handle() == handle:
            return user
    return None

# Return User with email if they exist in database, None otherwise.
def db_get_user_by_email(email):
    db = get_data()

    for user in db['users']:
        if user.get_email() == email:
            return user
