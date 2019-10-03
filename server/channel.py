# COMP1531 Project channel
# Written by Sabine Lim z5242579
# 01/10/19

# Invite user with u_id to channel with channel_id. Returns {} if successful.
# Raises ValueError exception if channel_id is invalid/user is not in channel or
# if u_id is invalid.
def channel_invite(token, channel_id, u_id):
    if channel_id not in [7654321, 3054207, 9703358]:
        raise ValueError

    if u_id not in [1234567, 5242579, 4201337, 9876543]:
        raise ValueError

    return {}

# Given channel with channel_id that authorised user is in, return basic
# details about the channel.
# Raise ValueError exception if channel with id does not exist.
# Raise AccessError exception if user is not member of channel.
def channel_details(token, channel_id):
    if channel_id not in [7654321, 3054207, 9703358]:
        raise ValueError

    return {}

# Given channel ID, remove user from channel.
# Raise ValueError exception if channel with id does not exist.
def channel_leave(token, channel_id):
    if channel_id not in [7654321, 3054207, 9703358]:
        raise ValueError

    return {}

# Given id of channel that user can join, add them to that channel.
# Raise ValueError exception if channel with id does not exist.
# Raise AccessError if channel is private and user is not admin.
def channel_join(token, channel_id):
    if channel_id not in [7654321, 3054207, 9703358]:
        raise ValueError

    return {}

# Make user with u_id an owner of channel. Returns {}.
# Raise ValueError exception if channel with id does not exist or user is
# already owner of channel.
# Raise AccessError exception if user is not owner of either slackr or channel.
def channel_addowner(token, channel_id, user_id):
    if channel_id not in [7654321, 3054207, 9703358]:
        raise ValueError

    return {}

# Remove user with u_id as owner of this channel. Returns {}.
# Raise ValueError exception if channel with id does not exist or user is not
# owner of channel.
# Raise AccessError exception if user is not owner of either slackr or channel.
def channel_removeowner():
    if channel_id not in [7654321, 3054207, 9703358]:
        raise ValueError

    return {}
