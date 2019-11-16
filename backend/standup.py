# COMP1531 Project standup stubs
# Written by Jake Tyler z5208823
# and Bridget McCarthy z5255505
# and Sabine Lim z5242579
# 3/10/19

from time import time

from .db import (
    User, Channel, Message, db_get_user_by_u_id, db_get_channel_by_channel_id,
    db_create_message, db_get_time_offset
)
from .auth import validate_token
from .error import ValueError, AccessError

############################## Standup Setup ########################################

def standup_setup(token, channel_id):

    user = validate_token(token)
    channel = db_get_channel_by_channel_id(channel_id)

    return user, channel

############################## Standup Start ########################################

# standup_start commands initiates 'length' seconds of standup and then returns
# 'length' seconds of stand up time.
# Raises ValueError when the channel_id is invalid or if there is already an
# active standup running in that channel.
# Raises AccessError when the channel exists but the user isnt in that channel.
# Return dictionary containing time the standup will finish.

def standup_start(token, channel_id, length):
    
    # sets up the user and channel
    user, channel = standup_setup(token, channel_id)
    
    adjusted_time = time() + db_get_time_offset()
    
    # check for errors
    standup_start_error(user, channel, adjusted_time, length)
    
    # Set standup to expire in 'length' seconds.
    time_finish = time() + length

    message = db_create_message(user, channel, "", time_finish)
    channel.set_standup(message)

    return {'time_finish': time_finish}

def standup_start_error(user, channel, adjusted_time, length):

    # new valueerror if length is wrong
    if (length <= 0):
        raise ValueError(description = "Standup time less then 0")

    # if the user isnt part of the channel
    if not channel.has_member(user):
        raise AccessError(description = "Authorised user is not member of that channel!")

    # if a standup is active and the time going to be added is less
    if channel.get_standup() is not None \
        and adjusted_time < channel.get_standup().get_time_created():
        raise ValueError(description = "An active standup is currently running in this channel!")

############################## Standup Active ########################################

# For a given channel, return whether a standup is active in it,
# and what time the standup finishes. If no standup is active,
# then time_finish returns None
def standup_active(token, channel_id):
    
    user, channel = standup_setup(token, channel_id)
    
    standup = channel.get_standup()
    adjusted_time = time() + db_get_time_offset()

    if standup is None or adjusted_time >= (standup.get_time_created()):
            return None

    return standup.get_time_created()

############################## Standup Send ########################################

# The standup_send function takes the users token, the desired channel_id
# and a message under 1000 characters and puts it in the standup_queue.
# Raises ValueError when the channel_id is invalid, message is over 1000
# characters or an active standup is not currently running in that channel.
# Raises AccessError when the channel exists but the user isnt in that channel.

def standup_send(token, channel_id, message):
    
    user, channel = standup_setup(token, channel_id)
    
    standup = channel.get_standup()
    adjusted_time = time() + db_get_time_offset()
    
    # error check
    standup_send_error(user, channel, adjusted_time, message, standup)

    old_text = standup.get_text()
    new_text = f"{old_text}{user.get_handle()}: {message} \n"

    standup.set_text(new_text)

    return {}

# error list
def standup_send_error(user, channel, adjusted_time, message, standup):
    
    if not channel.has_member(user):
        raise AccessError(description="Authorised user is not member of that channel!")

    if standup is None or adjusted_time >= (standup.get_time_created()):
        raise ValueError(description = "No active standup is currently running in this channel!")
    
    if len(message) > 1000:
        raise ValueError(description = "Message cannot be longer than 1000 characters!")
