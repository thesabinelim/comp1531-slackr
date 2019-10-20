# COMP1531 Project db
# Written by Sabine Lim z5242579
# 17/10/19

from ..server import get_data, get_secret
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
        self.channels = []
        self.tokens = []

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
    def get_channels(self):
        return self.channels
    def in_channel(self, channel_id):
        return channel_id in self.channels
    def get_tokens(self):
        return self.tokens
    def has_token(self, token):
        return token in self.tokens

    def set_email(self, new_email):
        self.email = new_email
    def set_password(self, new_password):
        self.hashpass = hash_password(new_password)
    def set_first_name(self, new_name_first):
        self.name_first = new_name_first
    def set_last_name(self, new_name_last):
        self.name_last = new_name_last
    def set_handle(self, new_handle):
        self.handle = new_handle
    def add_channel(self, channel_id):
        if channel_id in self.channels:
            return
        self.channels.append(channel_id)
    def remove_channel(self, channel_id):
        if channel_id not in self.channels:
            raise ValueError
        self.channels.remove(channel_id)
    def add_token(self, token):
        if token in self.tokens:
            return
        self.tokens.append(token)
    def remove_token(self, token):
        if token not in self.tokens:
            raise ValueError
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
    return None

#################
# channels data #
#################

class Channel:
    def __init__(self, channel_id, name, is_public):
        self.channel_id = channel_id
        self.name = name
        self.public = is_public
        self.owners = []
        self.members = []
        self.messages = []

    def get_channel_id(self):
        return self.channel_id
    def get_name(self):
        return self.name
    def is_public(self):
        return self.public
    def get_owners(self):
        return self.owners
    def get_members(self):
        return self.members
    def get_messages(self):
        return self.messages

    def set_name(self, new_name):
        self.name = new_name
    def set_public(self, is_public):
        self.public = is_public
    def add_owner(self, u_id):
        if u_id in self.owners:
            return
        self.owners.append(u_id)
    def remove_owner(self, u_id):
        if u_id not in self.owners:
            raise ValueError
        self.owners.remove(u_id)
    def add_member(self, u_id):
        if u_id in self.members:
            return
        self.members.append(u_id)
    def remove_member(self, u_id):
        if u_id not in self.members:
            raise ValueError
        self.members.remove(u_id)
    def add_message(self, message_id):
        if message_id in self.messages:
            return
        self.messages.append(message_id)
    def remove_message(self, message_id):
        if message_id not in self.messages:
            raise ValueError
        self.messages.remove(message_id)

# Create Channel with provided details and add to database, return channel_id.
def db_create_channel(name, is_public):
    db = get_data()

    channel_id = db['channels'][-1].get_channel_id() + 1

    channel = Channel(channel_id, name, is_public)
    db['channels'].append(channel)

    return channel_id

# Return Channel with channel_id if it exists in database, None otherwise.
def db_get_channel_by_channel_id(channel_id):
    db = get_data()

    for channel in db['channels']:
        if channel.get_channel_id() == channel_id:
            return channel
    return None

# Return Channel with name if it exists in database, None otherwise.
def db_get_channel_by_name(name):
    db = get_data()

    for channel in db['channels']:
        if channel.get_name() == name:
            return channel
    return None
