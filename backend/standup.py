# COMP1531 Project standup stubs
# Written by Jake Tyler z5208823
# and Bridget McCarthy z5255505
# and Sabine Lim z5242579
# 3/10/19

import time

from .db import (
    User, Channel, Message, db_get_user_by_u_id, db_get_channel_by_channel_id,
    db_create_message, db_get_time_offset
)
from .auth import validate_token
from .error import ValueError, AccessError

# standup_start commands initiates 15 minutes of standup and then returns
# 15 minutes of stand up time.
# Raises ValueError when the channel_id is invalid or if there is already an
# active standup running in that channel.
# Raises AccessError when the channel exists but the user isnt in that channel.
# Return dictionary containing time the standup will finish.
def standup_start(token, channel_id):
    u_id = validate_token(token)
    user = db_get_user_by_u_id(u_id)

    channel = db_get_channel_by_channel_id(channel_id)
    if channel is None:
        raise ValueError(description="Channel with channel_id does not exist in database!")

    if not channel.has_member(user):
        raise AccessError(description="Authorised user is not member of that channel!")
    adjusted_time = time.time() + db_get_time_offset()
    if channel.get_standup() is not None \
        and adjusted_time < channel.get_standup().get_time_created():
        raise ValueError(description="An active standup is currently running in this channel!")

    # Set standup to expire in 15 minutes.
    time_finish = time.time() + 15 * 60

    message = db_create_message(user, channel, "", time_finish)
    channel.set_standup(message)

    return {'time_finish': time_finish}

# The standup_send function takes the users token, the desired channel_id
# and a message under 1000 characters and puts it in the standup_queue.
# Raises ValueError when the channel_id is invalid, message is over 1000
# characters or an active standup is not currently running in that channel.
# Raises AccessError when the channel exists but the user isnt in that channel.
def standup_send(token, channel_id, message):
    u_id = validate_token(token)
    user = db_get_user_by_u_id(u_id)

    channel = db_get_channel_by_channel_id(channel_id)
    if channel is None:
        raise ValueError(description="Channel with channel_id does not exist in database!")

    if not channel.has_member(user):
        raise AccessError(description="Authorised user is not member of that channel!")

    standup = channel.get_standup()
    adjusted_time = time.time() + db_get_time_offset()
    if standup is None or adjusted_time >= (standup.get_time_created()):
        raise ValueError(description="No active standup is currently running in this channel!")

    if len(message) > 1000:
        raise ValueError(description="Message cannot be longer than 1000 characters!")

    old_text = standup.get_text()
    new_text = f"{old_text}{user.get_handle()}: {message} \n"

    standup.set_text(new_text)

    return {}
