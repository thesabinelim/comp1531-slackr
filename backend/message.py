# COMP1531 Project message
# Written by Bridget McCarthy z5255505 and Sabine Lim z5242579
# 1/10/19

from time import time

from .db import (
    Role, User, Channel, Message, db_create_message, db_get_user_by_u_id, 
    db_get_channel_by_channel_id, db_get_message_by_message_id
)
from .auth import validate_token
from .error import ValueError, AccessError

############################## Validate Message ########################################

def validate_message_text(text, time_now, time_sent):
    
    # if the message is empty
    if len(text) == 0:
        raise ValueError(description = "Message cannot be empty!")
    
    # if the message is over 1000 characters
    elif len(text) > 1000:
        raise ValueError(description = "Message cannot be longer than 1000 characters!")

    #
    if time_sent < time_now:
        raise ValueError(description = "Time sent cannot be in the past!")

############################ Validate Channel & Message ######################################

def validate_user_channel(token, channel_id):

    user = validate_token(token)
    channel = db_get_channel_by_channel_id(channel_id)

    return user, channel

def validate_user_message(token, message_id):
    
    user = validate_token(token)
    message = db_get_message_by_message_id(message_id)
    channel = message.get_channel()

    return user, channel, message


############################ Message Sendlater ######################################

# Send a message from authorised_user to the channel specified by channel_id.
# automatically at a specified time in the future. 
# Raises ValueError exception when channel_id doesn't exist, message is more
# than 1000 characters, or time_sent is a past time.
# Raises AccessError when user attempts to send message to channel they are not
# member of.
# Return dictionary containing message_id.

def message_sendlater(token, channel_id, text, time_sent):

    # authenticate user and channel
    user, channel = validate_user_channel(token, channel_id)

    # check for errors
    validate_message_text(text, time(), time_sent)
    message_sendlater_error(channel, user)
    
    message = db_create_message(user, channel, text, time_sent)

    return {'message_id': message.get_message_id()}

# error list
def message_sendlater_error(channel, user):
    
    # The user it not a member of the channel
    if not channel.has_member(user):
        raise AccessError(description = "User is not member of that channel!")

############################## Message Send ########################################

# Send a message from authorised_user to the channel specified by channel_id.
# Raises ValueError exception when the message is more than 1000 characters.
# Raises AccessError when user attempts to send message to channel they are not
# member of.
# Return dictionary containing message_id.

def message_send(token, channel_id, text):
    
    # authenticate user and channel
    user, channel = validate_user_channel(token, channel_id)

    now = time()
    
    # check for errors
    validate_message_text(text, now, now)
    message_send_error(channel, user)

    message = db_create_message(user, channel, text, now)

    return {'message_id': message.get_message_id()}

def message_send_error(channel, user):

    # The user it not a member of the channel
    if not channel.has_member(user):
        raise AccessError(description = "Authorised user is not member of that channel!")

############################## Message Remove ########################################

# Given a message_id for a message, this message is removed from the channel.
# Raises ValueError when the message_id no longer exists.
# Raises AccessError when these are NOT true:
#   message_id not sent by the authorised user,
#   AND user is not an owner of the channel or owner of the slack.
#   OR user is not in the channel containing the message.
# Return empty dictionary.

def message_remove(token, message_id):
    
    # authenticate and return user, channel and message
    user, channel, message = validate_user_message(token, message_id)

    # error checks
    message_remove_error(user, channel, message)
    
    channel.remove_message(message)

    return {}

# error list
def message_remove_error(user, channel, message):
    
    # if the user is not in the channel
    if not user.in_channel(channel):
        raise AccessError(description = "The authorised user is not the channel containing the message!")
    
    # if the message no longer exists
    if not channel.has_message(message):
        raise ValueError(description = "Message with message_id has already been deleted!")

    # if the user is not the person who sent the message
    if user != message.get_sender() and not channel.has_owner(user):
        raise AccessError(description = "The authorised user is not the sender of the message!")

############################## Message Edit ########################################

# Given a message, update it's text with new text.
# Raises ValueError when message with message_id does not exist.
# Raises AccessError if user is not member of channel containing message.
# Raises AccessError when message_id not sent by authorised user AND authorised
# user is not an admin or owner of either the channel or the Slackr.
# Return empty dictionary.

def message_edit(token, message_id, text):

    user, channel, message = validate_user_message(token, message_id)
    
    # error checks
    message_edit_error(user, channel, message, text)
    
    # if the text is empty remove, else reset it
    if text == "":
        channel.remove_message(message)
    else:
        message.set_text(text)

    return {}

# error list
def message_edit_error(user, channel, message, text):
    
    # new message is too long
    if len(text) > 1000:
        raise ValueError(description = "Message cannot be longer than 1000 characters!")
    
    # message does not exist
    if not message.get_channel().has_message(message):
        raise ValueError(description = "Message with message_id does not exist in channel!")

    # user is not a member of the channel
    if not channel.has_member(user):
        raise AccessError(description = "Authorised user is not member of that channel!")

    # user it not the sender
    if user != message.get_sender() and not channel.has_owner(user):
        raise AccessError(description = "Message was not sent by logged in user and user is \
                          not admin or owner!")

# Given a message within a channel the authorised user is part of, add a "react"
# to that particular message. 
# Raises ValueError when message_id is not a valid message within a channel 
# authorised user has joined.
# Raises ValueError when react_id is not valid.
# Raises ValueError when message for message_id already has a reaction with
# the react_id by user.
# Return empty dictionary.
def message_react(token, message_id, react_id):
    user = validate_token(token)

    message = db_get_message_by_message_id(message_id)
    if not message.get_channel().has_message(message):
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
    user = validate_token(token)

    message = db_get_message_by_message_id(message_id)
    if not message.get_channel().has_message(message):
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
    user = validate_token(token)

    message = db_get_message_by_message_id(message_id)
    if not message.get_channel().has_message(message):
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
    user = validate_token(token)

    message = db_get_message_by_message_id(message_id)
    if not message.get_channel().has_message(message):
        raise ValueError(description="Message with message_id does not exist in channel!")

    channel = message.get_channel()
    if not user.in_channel(channel):
        raise AccessError(description="Logged in user is not member of channel containing message with message_id!")

    if not channel.has_owner(user):
        raise ValueError(description="Logged in user is not admin or owner!")

    if not message.is_pinned():
        raise ValueError(description="Message with message_id is not pinned!")

    message.unpin()

    return {}
