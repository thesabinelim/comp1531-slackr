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
    def in_channel(self, channel):
        return channel in self.channels
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
    def join_channel(self, channel):
        if channel not in self.channels:
            self.channels.append(channel)
    def leave_channel(self, channel):
        if channel in self.channels:
            self.channels.remove(channel)
    def add_token(self, token):
        if token not in self.tokens:
            self.tokens.append(token)
    def remove_token(self, token):
        if token in self.tokens:
            self.tokens.remove(token)

# Create User with provided details and add to database, return u_id.
def db_create_user(email, password, name_first, name_last, handle, role):
    db = get_data()

    u_id = db['users'][-1].get_u_id() + 1
    hashpass = hash_password(password)

    user = User(u_id, email, hashpass, name_first, name_last, handle, role)
    db['users'].append(user)

    return u_id

# Return list of all Users in database.
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
    def has_owner(self, user):
        return user in self.owners
    def get_members(self):
        return self.members
    def has_member(self, user):
        return user in self.members
    def get_messages(self):
        return self.messages
    def has_message(self, message):
        return message in self.messages

    def set_name(self, new_name):
        self.name = new_name
    def set_public(self, is_public):
        self.public = is_public
    def add_owner(self, user):
        if user not in self.owners:
            self.owners.append(user)
    def remove_owner(self, user):
        if user in self.owners:
            self.owners.remove(user)
    def add_member(self, user):
        if user not in self.members:
            self.members.append(user)
    def remove_member(self, user):
        if user in self.members:
            self.members.remove(user)
    def add_message(self, message):
        if message not in self.messages:
            self.messages.append(message)
    def remove_message(self, message):
        if message_id in self.messages:
            self.messages.remove(message)

# Create Channel with provided details and add to database, return channel_id.
def db_create_channel(name, is_public):
    db = get_data()

    channel_id = db['channels'][-1].get_channel_id() + 1

    channel = Channel(channel_id, name, is_public)
    db['channels'].append(channel)

    return channel_id

# Return list of all Channels in database.
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
    def __init__(self, message_id, sender, channel, time_created):
        self.message_id = message_id
        self.sender = sender
        self.channel = channel
        self.time_created = time_created
        self.reacts = []
        self.pinned = False

    def get_message_id(self):
        return self.message_id
    def get_sender(self):
        return self.sender
    def get_channel(self):
        return self.channel
    def get_time_created(self):
        return self.time_created
    def get_react_by_react_id(self, react_id):
        for react in self.reacts:
            if react['react_id'] == react_id:
                return react
        return None
    def get_reacts(self):
        return self.reacts
    def is_pinned(self):
        return self.pinned

    # Ignore if user has already made that react.
    def add_react(self, react_id, user):
        react = self.get_react_by_react_id(react_id)
        if react == None:
            # This is the first react with this id.
            self.reacts.append({
                'react_id': react_id,
                'users': [user]
            })
        elif user not in react['users']:
            react['users'].append(user)
    # Ignore if user has not made that react or react does not exist.
    def remove_react(self, react_id, user):
        react = self.get_react_by_react_id(react_id)
        if react != None and user in react['users']:
            react['users'].remove(user)
    def pin(self):
        self.pinned = True
    def unpin(self):
        self.pinned = False

# Create Message with provided details and add to database, return Message.
def db_create_message(user, channel, time_created):
    db = get_data()

    message_id = db['messages'][-1].get_message_id() + 1

    message = Message(message_id, user, channel, time_created)
    db['messages'].append(message)

    return message

# Return list of all messages in database.
def db_get_all_messages():
    db = get_data()
    return db['messages']

# Return Message with message_id if it exists in database, None otherwise.
def db_get_message_by_message_id(message_id):
    db = get_data()

    for message in db['messages']:
        if message['message_id'] == message_id:
            return message
    return None
