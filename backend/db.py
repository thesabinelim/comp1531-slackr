# COMP1531 Project db
# Written by Sabine Lim z5242579
# 17/10/19

import enum
import copy

from ..server import get_data, get_secret
from auth import hash_password

##############
# users data #
##############

class Role(enum.Enum):
    owner = 1
    admin = 2
    member = 3

class User:
    def __init__(self, u_id, email, hashpass, name_first, name_last, handle, role):
        self.u_id = u_id
        self.email = email
        self.hashpass = hashpass
        self.name_first = name_first
        self.name_last = name_last
        self.handle = handle
        self.role = role
        self.channels = []
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
    def get_role(self):
        return self.role
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
    def set_role(self, new_role):
        self.role = new_role
    def join_channel(self, channel_id):
        if channel_id in self.channels:
            return
        self.channels.append(channel_id)
    def leave_channel(self, channel_id):
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
def db_create_user(email, password, name_first, name_last, handle, role):
    db = get_data()

    u_id = db['users'][-1].get_u_id() + 1
    hashpass = hash_password(password)

    user = User(u_id, email, hashpass, name_first, name_last, handle, role)
    db['users'].append(user)

    return u_id

# Return list of all Users in the database.
def db_get_all_users():
    db = get_data()
    return db['users']

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
    def has_owner(self, u_id):
        return u_id in self.owners
    def get_members(self):
        return self.members
    def has_member(self, u_id):
        return u_id in self.members
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

# Returns a list of all Channels in the database.
def db_get_all_channels():
    db = get_data()
    return db['channels']

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

#################
# messages data #
#################

class Message:
    def __init__(self, message_id, u_id, channel_id, time_created):
        self.message_id = message_id
        self.u_id = u_id
        self.channel_id = channel_id
        self.time_created = time_created
        self.reacts = []
        self.pinned = False

    def get_message_id(self):
        return self.message_id
    def get_u_id(self):
        return self.u_id
    def get_channel_id(self):
        return self.channel_id
    def get_time_created(self):
        return self.time_created
    def get_react_by_react_id(self, react_id):
        for react in self.reacts:
            if react['react_id'] == react_id:
                return react
        return None
    def get_reacts(self, u_id):
        return self.reacts
    def is_pinned(self):
        return self.pinned

    # Ignore if user has already made that react.
    def add_react(self, react_id, u_id):
        react = self.get_react_by_react_id(react_id)
        if react == None:
            # This is the first react with this id.
            self.reacts.append({
                'react_id': react_id,
                'u_ids': [u_id]
            })
            return
        if u_id not in react['u_ids']:
            react['u_ids'].append(u_id)
    # Ignore if user has not made that react or react does not exist.
    def remove_react(self, react_id, u_id):
        react = self.get_react_by_react_id(react_id)
        if react == None:
            return
        if u_id in react['u_ids']:
            react['u_ids'].remove(u_id)
    def pin(self):
        self.pinned = True
    def unpin(self):
        self.pinned = False

# Create Message with provided details and add to database, return message_id.
def db_create_message(u_id, channel_id, time_created):
    pass

# Return Message with message_id if it exists in database, None otherwise.
def db_get_message_by_message_id(message_id):
    pass
