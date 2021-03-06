# COMP1531 Project db
# Written by Sabine Lim z5242579
# 17/10/19

from flask import request
from os import urandom
from hashlib import pbkdf2_hmac
from enum import Enum
from time import time, sleep
from pickle import load as pickle_load, dump as pickle_dump
from threading import Thread

from .utils import random_string
from .error import ValueError

############
# database #
############

data = None

def commit_data():
    db_file = open("backend/db.p", "wb")
    pickle_dump(data, db_file)
    db_file.close()

def commit_data_timer():
    while True:
        commit_data()
        sleep(60)

def init_data():
    global data
    try:
        db_file = open("backend/db.p", "rb")
        data = pickle_load(db_file)
        db_file.close()
        print('load success!')
        print(data)
    except FileNotFoundError:
        reset_data()
        print('database reset!')
    Thread(target=commit_data_timer).start()

def get_data():
    global data
    return data

def get_secret():
    return get_data()['secret']

def get_salt():
    return get_data()['salt']

def reset_secret():
    get_data()['secret'] = random_string(128)

def reset_salt():
    get_data()['salt'] = urandom(32)

def reset_data():
    global data
    data = {
        'users': [],
        'channels': [],
        'messages': [],
        'reset_requests': [],
        'time_offset': 0,
        'backend_url': 'http://localhost:5001/',
        'secret': None,
        'salt': None,
    }
    reset_secret()
    reset_salt()

####################
# Password hashing #
####################

# Return salted hash of password supplied.
def hash_password(password):
    salt = get_salt()
    return pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

###############
# URL Routing #
###############

def db_set_backend_url(backend_url):
    db = get_data()
    db['backend_url'] = backend_url

def db_get_backend_url():
    db = get_data()
    return db['backend_url']

#####################
# Time manipulation #
#####################
# Used for functions that depend on time to test.
# Their calculations for time() will add get_db_time_offset() on the end.
# Outside of testing, this will always be zero, but when testing this allows us
# to modify the time to test more easily.
def db_add_time_offset(seconds):
    db = get_data()
    db['time_offset'] += seconds

def db_reset_time_offset():
    db = get_data()
    db['time_offset'] = 0

def db_get_time_offset():
    db = get_data()
    return db['time_offset']

##############
# users data #
##############

class Role(Enum):
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
        self.profile_img_url = None
        self.role = role
        self.channels = []
        self.tokens = []

    def to_dict(self):
        return {
            'u_id': self.u_id,
            'email': self.email,
            'name_first': self.name_first,
            'name_last': self.name_last,
            'handle_str': self.handle,
            'profile_img_url': self.profile_img_url
        }
    def to_dict_short(self):
        return {
            'u_id': self.u_id,
            'name_first': self.name_first,
            'name_last': self.name_last,
            'profile_img_url': self.profile_img_url
        }
    def get_u_id(self):
        return self.u_id
    def get_email(self):
        return self.email
    def password_matches(self, password):
        hashpass = hash_password(password)
        return hashpass == self.hashpass
    def get_first_name(self):
        return self.name_first
    def get_last_name(self):
        return self.name_last
    def get_handle(self):
        return self.handle
    def get_profile_img_url(self):
        return self.profile_img_url
    def get_slackr_role(self):
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
    def set_profile_img_url(self, new_profile_img_url):
        self.profile_img_url = new_profile_img_url
    def set_slackr_role(self, new_role):
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

# Create User with provided details and add to database, return User.
def db_create_user(email, password, name_first, name_last, handle, role):
    db = get_data()

    if db['users'] == []:
        u_id = 1
    else:
        u_id = db['users'][-1].get_u_id() + 1

    hashpass = hash_password(password)

    user = User(u_id, email, hashpass, name_first, name_last, handle, role)
    db['users'].append(user)

    return user

# Return list of all Users in database.
def db_get_all_users():
    db = get_data()
    return db['users']

# Return User with u_id if they exist in database, raise ValueError otherwise.
def db_get_user_by_u_id(u_id, error=True):
    db = get_data()

    for user in db['users']:
        if user.get_u_id() == u_id:
            return user
    if error:
        raise ValueError(description=f"User with u_id {u_id} does not exist!")
    return None

# Return User with handle if they exist in database, raise ValueError otherwise.
def db_get_user_by_handle(handle, error=True):
    db = get_data()

    for user in db['users']:
        if user.get_handle() == handle:
            return user
    if error:
        raise ValueError(description=f"User with handle {handle} does not exist!")
    return None

# Return User with email if they exist in database, raise ValueError otherwise.
def db_get_user_by_email(email, error=True):
    db = get_data()

    for user in db['users']:
        if user.get_email() == email:
            return user
    if error:
        raise ValueError(description=f"User with email {email} does not exist!")
    return None

# Returns the images folder that holds user's uploded photos
def db_get_image_folder():
    return 'imgurls'

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
        self.standup = None

    def to_dict(self):
        return {
            'channel_id': self.channel_id,
            'name': self.name
        }
    def get_channel_id(self):
        return self.channel_id
    def get_name(self):
        return self.name
    def is_public(self):
        return self.public
    def get_true_owners(self):
        return self.owners
    def has_true_owner(self, user):
        return user in self.owners
    def get_owners(self):
        owners = []
        for member in self.members:
            if member in self.owners or member.get_slackr_role() == Role.owner \
                or member.get_slackr_role() == Role.admin:
                owners.append(member)
        return owners
    def has_owner(self, user):
        is_owner = user in self.owners
        if user in self.members:
            if user.get_slackr_role() == Role.owner \
                or user.get_slackr_role() == Role.admin:
                is_owner = True
        return is_owner
    def get_members(self):
        return self.members
    def has_member(self, user):
        return user in self.members
    def get_messages(self):
        return self.messages
    def has_message(self, message):
        return message in self.messages
    def get_standup(self):
        return self.standup

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
    # Insert in descending order of time_created
    def add_message(self, message):
        if message in self.messages:
            return
        i = 0
        for m in self.messages:
            if message.get_time_created() > m.get_time_created():
                break
            i += 1
        self.messages.insert(i, message)
    def remove_message(self, message):
        if message in self.messages:
            self.messages.remove(message)
    def set_standup(self, message):
        self.standup = message

# Create Channel with provided details and add to database, return Channel.
def db_create_channel(name, is_public):
    db = get_data()

    if db['channels'] == []:
        channel_id = 1
    else:
        channel_id = db['channels'][-1].get_channel_id() + 1

    channel = Channel(channel_id, name, is_public)
    db['channels'].append(channel)

    return channel

# Return list of all Channels in database.
def db_get_all_channels():
    db = get_data()
    return db['channels']

# Return Channel with channel_id if it exists in database, raise ValueError otherwise.
def db_get_channel_by_channel_id(channel_id, error=True):
    db = get_data()

    for channel in db['channels']:
        if channel.get_channel_id() == channel_id:
            return channel
    if error:
        raise ValueError(description=f"Channel with channel_id {channel_id} does not exist!")
    return None

#################
# messages data #
#################

def react_to_dict(react, u_id):
    return {
        'react_id': react['react_id'],
        'u_ids': react['u_ids'],
        'is_this_user_reacted': u_id in react['u_ids']
    }

def reacts_to_dict(reacts, u_id):
    result = []
    for react in reacts:
        result.append(react_to_dict(react, u_id))
    return result

class Message:
    def __init__(self, message_id, sender, channel, text, time_created):
        self.message_id = message_id
        self.sender = sender
        self.channel = channel
        self.text = text
        self.time_created = time_created
        self.reacts = []
        self.pinned = False

    def to_dict(self, u_id):
        return {
            'message_id': self.message_id,
            'u_id': self.sender.u_id,
            'message': self.text,
            'time_created': self.time_created,
            'reacts': reacts_to_dict(self.reacts, u_id),
            'is_pinned': self.pinned
        }
    def get_message_id(self):
        return self.message_id
    def get_sender(self):
        return self.sender
    def get_channel(self):
        return self.channel
    def get_text(self):
        return self.text
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

    def set_text(self, new_text):
        self.text = new_text
    # Raise ValueError if user has already made that react.
    def add_react(self, user, react_id):
        react = self.get_react_by_react_id(react_id)
        if react is None:
            # This is the first react with this id.
            self.reacts.append({
                'react_id': react_id,
                'u_ids': [user.get_u_id()]
            })
        elif user.get_u_id() in react['u_ids']:
            raise ValueError(description="User has already made that react!")
        else:
            react['u_ids'].append(user.get_u_id())
    # Raise ValueError if user has not made that react or react does not exist.
    def remove_react(self, user, react_id):
        react = self.get_react_by_react_id(react_id)
        if react is None:
            raise ValueError(description="React with react_id has not been made!")
        if user.get_u_id() not in react['u_ids']:
            raise ValueError(description="User has not made that react!")
        react['u_ids'].remove(user.get_u_id())
        if len(react['u_ids']) == 0:
            self.reacts.remove(react)
    def pin(self):
        self.pinned = True
    def unpin(self):
        self.pinned = False

# Create Message with provided details and add to database, return Message.
def db_create_message(user, channel, text, time_created):
    db = get_data()

    if db['messages'] == []:
        message_id = 1
    else:
        message_id = db['messages'][-1].get_message_id() + 1

    message = Message(message_id, user, channel, text, time_created)
    channel.add_message(message)
    db['messages'].append(message)

    return message

# Return list of all Messages in database.
def db_get_all_messages():
    db = get_data()
    return db['messages']

# Return Message with message_id if it exists in database, raise ValueError otherwise.
def db_get_message_by_message_id(message_id, error=True):
    db = get_data()

    for message in db['messages']:
        if message.get_message_id() == message_id:
            return message
    if error:
        raise ValueError(description=f"Message with message_id {message_id} does not exist!")
    return None

#######################
# reset_requests data #
#######################

class Reset_Request:
    def __init__(self, reset_code, user, time_expires):
        self.reset_code = reset_code
        self.user = user
        self.time_expires = time_expires

    def get_reset_code(self):
        return self.reset_code
    def get_user(self):
        return self.user
    def get_time_expires(self):
        return self.time_expires
    def is_expired(self):
        return self.time_expires <= time()

    def set_time_expires(self, new_time_expires):
        self.time_expires = new_time_expires
    def expire(self):
        self.time_expires = time()

# Create Reset_Request with provided details and add to database, return
# Reset_Request.
def db_create_reset_request(user, time_expires):
    db = get_data()

    # Create unique reset_code
    unique = False
    while not unique:
        reset_code = random_string(6)
        unique = True
        for reset_request in db['reset_requests']:
            if reset_request.get_reset_code() == reset_code:
                unique = False

    reset_request = Reset_Request(reset_code, user, time_expires)
    db['reset_requests'].append(reset_request)

    return reset_request

# Return list of all Reset_Requests in database.
def db_get_all_reset_requests():
    db = get_data()
    return db['reset_requests']

# Return Reset_Request with reset_code if it exists in database, None otherwise.
def db_get_reset_request_by_reset_code(reset_code):
    db = get_data()

    for reset_request in db['reset_requests']:
        if reset_request.get_reset_code() == reset_code:
            return reset_request
    return None
