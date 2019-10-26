# COMP1531 Project message
# Written by Bridget McCarthy z5255505 and Sabine Lim z5242579
# 1/10/19

import time

from .db import (
    Role, User, Channel, Message, db_create_message, db_get_user_by_u_id, 
    db_get_channel_by_channel_id, db_get_message_by_message_id
)
from .auth import validate_token
from .error import ValueError, AccessError

# Send a message from authorised_user to the channel specified by channel_id.
# automatically at a specified time in the future. 
# Raises ValueError exception when channel_id doesn't exist, message is more
# than 1000 characters, or time_sent is a past time.
# Raises AccessError when user attempts to send message to channel they are not
# member of.
# Return dictionary containing message_id.
def message_sendlater(token, channel_id, text, time_sent):
    u_id = validate_token(token)
    user = db_get_user_by_u_id(u_id)

    if len(text) == 0:
        raise ValueError(description="Message cannot be empty!")

    if len(text) > 1000:
        raise ValueError(description="Message cannot be longer than 1000 characters!")

    now = time.time()
    if time_sent < now:
        raise ValueError(description="Time sent cannot be in the past!")

    channel = db_get_channel_by_channel_id(channel_id)
    if channel is None:
        raise ValueError(description="Channel with channel_id does not exist!")

    if not channel.has_member(user):
        raise AccessError(description="Authorised user is not member of that channel!")

    message = db_create_message(user, channel, text, time_sent)
    message_id = message.get_message_id()

    return {'message_id': message_id}

# Send a message from authorised_user to the channel specified by channel_id.
# Raises ValueError exception when the message is more than 1000 characters.
# Raises AccessError when user attempts to send message to channel they are not
# member of.
# Return dictionary containing message_id.
def message_send(token, channel_id, text):
    u_id = validate_token(token)
    user = db_get_user_by_u_id(u_id)

    if len(text) == 0:
        raise ValueError(description="Message cannot be empty!")

    if len(text) > 1000:
        raise ValueError(description="Message cannot be longer than 1000 characters!")

    channel = db_get_channel_by_channel_id(channel_id)
    if channel is None:
        raise ValueError(description="Channel with channel_id does not exist!")

    if not channel.has_member(user):
        raise AccessError(description="Authorised user is not member of that channel!")

    now = time.time()
    message = db_create_message(user, channel, text, now)
    message_id = message.get_message_id()

    return {'message_id': message_id}

# Given a message_id for a message, this message is removed from the channel.
# Raises ValueError when the message_id no longer exists.
# Raises AccessError when these are NOT true:
#   message_id not sent by the authorised user,
#   AND user is not an owner of the channel or owner of the slack.
#   OR user is not in the channel containing the message.
# Return empty dictionary.
def message_remove(token, message_id):
    u_id = validate_token(token)
    user = db_get_user_by_u_id(u_id)

    message = db_get_message_by_message_id(message_id)
    if message is None:
        raise ValueError(description="Message with message_id does not exist!")

    sender = message.get_sender()
    channel = message.get_channel()

    if not user.in_channel(channel):
        raise AccessError(description="The authorised user is not the channel containing the message!")

    if not channel.has_message(message):
        raise ValueError(description="Message with message_id has already been deleted!")

    if user != sender and not channel.has_owner(user):
        raise AccessError(description="The authorised user is not the sender of the message!")

    channel.remove_message(message)

    return {}

# Given a message, update it's text with new text.
# Raises ValueError when message with message_id does not exist.
# Raises AccessError if user is not member of channel containing message.
# Raises AccessError when message_id not sent by authorised user AND authorised
# user is not an admin or owner of either the channel or the Slackr.
# Return empty dictionary.
def message_edit(token, message_id, text):
    u_id = validate_token(token)
    user = db_get_user_by_u_id(u_id)

    if len(text) == 0:
        raise ValueError(description="Message cannot be empty!")

    if len(text) > 1000:
        raise ValueError(description="Message cannot be longer than 1000 characters!")

    message = db_get_message_by_message_id(message_id)
    if message is None or not message.get_channel().has_message(message):
        raise ValueError(description="Message with message_id does not exist!")

    channel = message.get_channel()

    if not channel.has_member(user):
        raise AccessError(description="Authorised user is not member of that channel!")

    if user != message.get_sender() and not channel.has_owner(user):
        raise AccessError(description="Message was not sent by logged in user and user is \
            not admin or owner!")

    message.set_text(text)

    return {}

# Given a message within a channel the authorised user is part of, add a "react"
# to that particular message. 
# Raises ValueError when message_id is not a valid message within a channel 
# authorised user has joined.
# Raises ValueError when react_id is not valid.
# Raises ValueError when message for message_id already has a reaction with
# the react_id by user.
# Return empty dictionary.
def message_react(token, message_id, react_id):
    u_id = validate_token(token)
    user = db_get_user_by_u_id(u_id)

    message = db_get_message_by_message_id(message_id)
    if message is None or not message.get_channel().has_message(message):
        raise ValueError(description="Message with message_id is not a valid message within a channel authorised user has joined!")

    channel = message.get_channel()
    if not channel.has_member(user):
        raise ValueError(description="Message with message_id is not a valid message within a channel authorised user has joined!")

    try:
        message.add_react(user, react_id)
    except ValueError:
        raise ValueError(description="Message already has a reaction with react_id by logged in user!")

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
    u_id = validate_token(token)
    user = db_get_user_by_u_id(u_id)

    message = db_get_message_by_message_id(message_id)
    if message is None or not message.get_channel().has_message(message):
        raise ValueError(description="Message with message_id is not a valid message within a channel authorised user has joined!")

    channel = message.get_channel()
    if not channel.has_member(user):
        raise ValueError(description="Message with message_id is not a valid message within a channel authorised user has joined!")

    try:
        message.remove_react(user, react_id)
    except ValueError:
        raise ValueError(description="Message does not have a reaction with react_id by logged in user!")

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
    u_id = validate_token(token)
    user = db_get_user_by_u_id(u_id)

    message = db_get_message_by_message_id(message_id)
    if message is None or not message.get_channel().has_message(message):
        raise ValueError(description="Message with message_id does not exist!")

    channel = message.get_channel()
    if not user.in_channel(channel):
        raise AccessError(description="Logged in user is not member of channel containing message with message_id!")

    if not channel.has_owner(user):
        raise ValueError(description="Logged in user is not admin or owner!")

    if message.is_pinned():
        raise ValueError(description="Message with message_id is already pinned!")

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
    u_id = validate_token(token)
    user = db_get_user_by_u_id(u_id)

    message = db_get_message_by_message_id(message_id)
    if message is None or not message.get_channel().has_message(message):
        raise ValueError(description="Message with message_id does not exist!")

    channel = message.get_channel()
    if not user.in_channel(channel):
        raise AccessError(description="Logged in user is not member of channel containing message with message_id!")

    if not channel.has_owner(user):
        raise ValueError(description="Logged in user is not admin or owner!")

    if not message.is_pinned():
        raise ValueError(description="Message with message_id is not pinned!")

    message.unpin()

    return {}
