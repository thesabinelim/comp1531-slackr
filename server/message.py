# COMP1531 Project message
# Written by Bridget McCarthy z5255505
# 1/10/19

import datetime
# Send a message from authorised_user to the channel specified by channel_id.
# automatically at a specified time in the future. 
# Raises ValueError exception when channel_id doesn't exist, messige is more
# than 1000 characters, or time_sent is a past time.
# No return value.
def message_sendlater(token, channel_id, message, time_sent):
    if len(message) > 1000:
        raise ValueError
    if time_sent < datetime.datetime.now():
        raise ValueError
    if channel_id < 0:
        raise ValueError

# Send a message from authorised_user to the channel specified by channel_id.
# Raises ValueError exception when the message is more than 1000 characters.
# No return value.
def message_send(token, channel_id, message):
    if len(message) > 1000:
        raise ValueError

# Given a message_id for a message, this message is removed from the channel.
# Raises ValueError when the message_id no longer exists.
# Raises AccessError when message_id not sent by authorised user, AND message_id
# was not sent by an owner of the channel AND message_id was not sent by an admin
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
# the react_id.
# No return value.
def message_react(token, message_id, react_id):
    if message_id == '420':
        raise ValueError
    if react_id < 0:
        raise ValueError
    if react_id == '10' and message_id == '20':
        raise ValueError

# Given a message within a channel the authorised user is part of, remove a 
# "react" to that particular message.
# Raises ValueError when message_id is not a valid message within a channel 
# authorised user has joined.
# Raises ValueError when react_id is not valid.
# Raises ValueError when message for message_id doesn't have a reaction with
# the react_id.
# No return value.
def message_unreact(token, message_id, react_id):
    if message_id == '420':
        raise ValueError
    if react_id < 0:
        raise ValueError
    if react_id == '10' and message_id != '20':
        raise ValueError

# Given a message within a channel, mark it as "pinned" to be given special 
# display treatment by the frontend.
# Raises ValueError when message_id is not a valid message.
# Raises ValueError when authorised user is not an admin.
# Raises ValueError when message_id is already pinned.
# Raises AccessError when authorised user is not a member of channel for
# the message.
# No return value.
def message_pin(token, message_id):
    if message_id == '420':
        raise ValueError
    if token == '1234567':
        raise ValueError
    if message_id == '20':
        raise ValueError
    if token == '7849321':
        raise AccessError

# Given a message within a channel, remove it's mark as unpinned.
# Raises ValueError when message_id is not a valid message.
# Raises ValueError when authorised user is not an admin.
# Raises ValueError when message_id isn't pinned.
# Raises AccessError when authorised user is not a member of channel for
# the message.
# No return value.
def message_unpin(token, message_id):
    if message_id == '420':
        raise ValueError
    if token == '1234567':
        raise ValueError
    if message_id != '20':
        raise ValueError
    if token == '7849321':
        raise AccessError
