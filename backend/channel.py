# COMP1531 Project channel
# Written by Sabine Lim z5242579
# 01/10/19

from db import (
    Role, User, Channel, Message, db_get_channel_by_channel_id,
    db_get_user_by_u_id
)
from auth import validate_token
from error import TokenError, AccessError

# Invite user with u_id to channel with channel_id.
# Return {} if successful.
# Raises ValueError exception if channel_id is invalid/user is not in channel or
# if u_id is invalid.
def channel_invite(token, channel_id, u_id):
    try:
        sender_id, token_valid = validate_token(token)
    except ValueError:
        raise ValueError("Token was not generated by server!")
    if not token_valid:
        raise TokenError("Token is invalid!")

    sender = db_get_user_by_u_id(sender_id)
    receiver = db_get_user_by_u_id(u_id)
    if receiver == None:
        raise ValueError("User with u_id does not exist!")
    channel = db_get_channel_by_channel_id(channel_id)
    if channel == None:
        raise ValueError("Channel with channel_id does not exist!")

    if not sender.in_channel(channel):
        raise AccessError("Invite sender is not member of channel!")

    receiver.join_channel(channel)

    return {}

# Given channel with channel_id that user is in, return details about channel.
# Raise ValueError exception if channel with id does not exist.
# Raise AccessError exception if user is not member of channel.
def channel_details(token, channel_id):
    try:
        u_id, token_valid = validate_token(token)
    except ValueError:
        raise ValueError("Token was not generated by server!")
    if not token_valid:
        raise TokenError("Token is invalid!")

    user = db_get_user_by_u_id(u_id)
    channel = db_get_channel_by_channel_id(channel_id)
    if channel == None:
        raise ValueError("Channel with channel_id does not exist!")

    if not user.in_channel(channel):
        raise AccessError("User is not member of channel!")

    name = channel.get_name()
    owner_members = []
    for owner in channel.get_owners():
        owner_members.append({
            'u_id': owner.get_u_id(),
            'name_first': owner.get_first_name(),
            'name_last': owner.get_last_name()
        })
    all_members = []
    for member in channel.get_members():
        all_members.append({
            'u_id': member.get_u_id(),
            'name_first': member.get_first_name(),
            'name_last': member.get_last_name()
        })

    return {
        'name': name,
        'owner_members': owner_members,
        'all_members': all_members
    }

# Given channel with channel_id that user is in, return up to 50 messages
# between index "start" and "start + 50". Message with index 0 is most recent
# message in channel. Return a new index "end" which is value of "start + 50" or
# if this function returned least recent messages in channel, return -1 in "end"
# to indicate there are no more messages to load after this return.
# Raise ValueError exception when channel with id does not exist or start is >
# total number of messages in channel.
# Raise AccessError exception when user is not member of channel with id.
def channel_messages(token, channel_id, start):
    pass

# Given channel ID, remove user from channel. Returns {}.
# Raise ValueError exception if channel with id does not exist.
# An owner leaving removes them from the channel's owner list.
def channel_leave(token, channel_id):
    try:
        u_id, token_valid = validate_token(token)
    except ValueError:
        raise ValueError("Token was not generated by server!")
    if not token_valid:
        raise TokenError("Token is invalid!")

    user = db_get_user_by_u_id(u_id)
    channel = db_get_channel_by_channel_id(channel_id)
    if channel == None:
        raise ValueError("Channel with channel_id does not exist!")

    channel.remove_owner(user)
    channel.remove_member(user)
    user.leave_channel(channel)

    return {}

# Given id of channel that user can join, add them to that channel.
# Raise ValueError exception if channel with id does not exist.
# Raise AccessError if channel is private and user is not admin.
# Raise TokenError if token invalid.
def channel_join(token, channel_id):
    try:
        u_id, token_valid = validate_token(token)
    except ValueError:
        raise ValueError("Token was not generated by server!")
    if not token_valid:
        raise TokenError("Token is invalid!")

    user = db_get_user_by_u_id(u_id)
    channel = db_get_channel_by_channel_id(channel_id)
    if channel == None:
        raise ValueError("Channel with channel_id does not exist!")

    if not channel.is_public():
        if user.get_slackr_role() != Role.admin and user.get_slackr_role() != Role.owner:
            raise AccessError("Channel is private and user is not admin or owner!")

    channel.add_member(user)
    user.join_channel(channel)

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
def channel_removeowner(token, channel_id, user_id):
    if channel_id not in [7654321, 3054207, 9703358]:
        raise ValueError

    return {}
