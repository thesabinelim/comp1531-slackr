# COMP1531 Project channel
# Written by Sabine Lim z5242579
# 01/10/19

# Invite user with u_id to channel with channel_id. Returns {} if successful.
# Raises ValueError exception if channel_id is invalid/user is not in channel or
# if u_id is invalid.
def channel_invite(token, channel_id, u_id):
    return {}

# Given id of channel that user can join, add them to that channel.
# Raise ValueError exception if channel with id does not exist.
# Raise AccessError if channel is private and user is not admin.
def channel_join(token, channel_id):
    return {}

# Given channel ID, remove user from channel.
# Raise ValueError exception if channel with id does not exist.
def channel_leave(token, channel_id):
    if channel_id == 7654321:
        return {}
    elif channel_id == 3054207:
        return {}
    elif channel_id == 9703358:
        return {}
    return {}
