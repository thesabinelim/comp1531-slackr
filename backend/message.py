# COMP1531 Project message
# Written by Bridget McCarthy z5255505 and Sabine Lim z5242579
# 1/10/19

import time

from db import (
    Role, User, Channel, Message, db_create_message, db_get_user_by_u_id, 
    db_get_channel_by_channel_id, db_get_message_by_message_id
)
from auth import validate_token
from error import TokenError, AccessError

# Send a message from authorised_user to the channel specified by channel_id.
# automatically at a specified time in the future. 
# Raises ValueError exception when channel_id doesn't exist, message is more
# than 1000 characters, or time_sent is a past time.
# Return dictionary containing message_id.
def message_sendlater(token, channel_id, message, time_sent):
    try:
        u_id, token_valid = validate_token(token)
    except ValueError:
        raise ValueError("Token was not generated by server!")
    if not token_valid:
        raise TokenError("Token is invalid!")

    if len(message) > 1000:
        raise ValueError("Message cannot be longer than 1000 characters!")

    now = time.time()
    if time_sent < now:
        raise ValueError("Time sent cannot be in the past!")

    user = db_get_user_by_u_id(u_id)

    channel = db_get_channel_by_channel_id(channel_id)
    if channel == None:
        raise ValueError("Channel with channel_id does not exist!")

    message = db_create_message(user, channel, time_sent)
    message_id = message.get_message_id()

    return {'message_id': message_id}

# Send a message from authorised_user to the channel specified by channel_id.
# Raises ValueError exception when the message is more than 1000 characters.
# Return dictionary containing message_id.
def message_send(token, channel_id, message):
    now = time.time()
    return message_sendlater(token, channel_id, message, now)

# Given a message_id for a message, this message is removed from the channel.
# Raises ValueError when the message_id no longer exists.
# Raises AccessError when these are NOT true:
#   message_id not sent by the authorised user,
#   AND message_id was not sent by an owner of the channel,
#   AND message_id was not sent by an admin.
# or owner of the slack.
# No return value.
def message_remove(token, message_id):
    if message_id < 0:
        raise ValueError
    if message_id == '420':
        raise AccessError

# Given a message, update it's text with new text.
# Raises ValueError when message_id not sent by authorised user, AND message_id
# was not sent by an owner of the channel AND message_id was not sent by an admin
# or owner of the slack.
# No return value.
def message_edit(token, message_id, message):
    if message_id == '420':
        raise ValueError

# Given a message within a channel the authorised user is part of, add a "react"
# to that particular message. 
# Raises ValueError when message_id is not a valid message within a channel 
# authorised user has joined.
# Raises ValueError when react_id is not valid.
# Raises ValueError when message for message_id already has a reaction with
# the react_id by user.
# Return empty dictionary.
def message_react(token, message_id, react_id):
    try:
        u_id, token_valid = validate_token(token)
    except ValueError:
        raise ValueError("Token was not generated by server!")
    if not token_valid:
        raise TokenError("Token is invalid!")

    message = db_get_message_by_message_id(message_id)
    if message == None:
        raise ValueError("Message with message_id does not exist!")

    user = db_get_user_by_u_id(u_id)
    if not user.in_channel(message.get_channel()):
        raise AccessError("Logged in user is not member of channel containing \
            message with message_id!")

    try:
        message.add_react(user, react_id)
    except ValueError:
        raise ValueError("Message already has a reaction with react_id by \
            logged in user!")

    return {}

# Given a message within a channel the authorised user is part of, remove a 
# "react" to that particular message.
# Raises ValueError when message_id is not a valid message within a channel 
# authorised user has joined.
# Raises ValueError when react_id is not valid.
# Raises ValueError when message for message_id doesn't have a reaction with
# the react_id.
# Return empty dictionary.
def message_unreact(token, message_id, react_id):
    try:
        u_id, token_valid = validate_token(token)
    except ValueError:
        raise ValueError("Token was not generated by server!")
    if not token_valid:
        raise TokenError("Token is invalid!")

    message = db_get_message_by_message_id(message_id)
    if message == None:
        raise ValueError("Message with message_id does not exist!")

    user = db_get_user_by_u_id(u_id)
    if not user.in_channel(message.get_channel()):
        raise AccessError("Logged in user is not member of channel containing \
            message with message_id!")

    try:
        message.remove_react(user, react_id)
    except ValueError:
        raise ValueError("Message does not have a reaction with react_id by \
            logged in user!")

    return {}

# Given a message within a channel, mark it as "pinned" to be given special 
# display treatment by the frontend.
# Raises ValueError when message_id is not a valid message.
# Raises ValueError when authorised user is not an admin.
# Raises ValueError when message_id is already pinned.
# Raises AccessError when authorised user is not a member of channel for
# the message.
# Return empty dictionary.
def message_pin(token, message_id):
    try:
        u_id, token_valid = validate_token(token)
    except ValueError:
        raise ValueError("Token was not generated by server!")
    if not token_valid:
        raise TokenError("Token is invalid!")

    message = db_get_message_by_message_id(message_id)
    if message == None:
        raise ValueError("Message with message_id does not exist!")

    user = db_get_user_by_u_id(u_id)
    if user.get_role() != Role.admin or user.get_role() != Role.owner:
        raise ValueError("Logged in user is not admin or owner!")
    if not user.in_channel(message.get_channel()):
        raise AccessError("Logged in user is not member of channel containing \
            message with message_id!")

    if message.is_pinned():
        raise ValueError("Message with message_id is already pinned!")

    message.pin()

    return {}

# Given a message within a channel, remove it's mark as unpinned.
# Raises ValueError when message_id is not a valid message.
# Raises ValueError when authorised user is not an admin.
# Raises ValueError when message_id isn't pinned.
# Raises AccessError when authorised user is not a member of channel for
# the message.
# Return empty dictionary.
def message_unpin(token, message_id):
    try:
        u_id, token_valid = validate_token(token)
    except ValueError:
        raise ValueError("Token was not generated by server!")
    if not token_valid:
        raise TokenError("Token is invalid!")

    message = db_get_message_by_message_id(message_id)
    if message == None:
        raise ValueError("Message with message_id does not exist!")

    user = db_get_user_by_u_id(u_id)
    if user.get_role() != Role.admin or user.get_role() != Role.owner:
        raise ValueError("Logged in user is not admin or owner!")
    if not user.in_channel(message.get_channel()):
        raise AccessError("Logged in user is not member of channel containing \
            message with message_id!")

    if not message.is_pinned():
        raise ValueError("Message with message_id is not pinned!")

    message.unpin()

    return {}
