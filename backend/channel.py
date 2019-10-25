# COMP1531 Project channel
# Written by Sabine Lim z5242579, Bridget McCarthy z5255505
# and Eric Lin z5257305
# 23/10/19

import time

from .db import (
    Role, User, Channel, Message, db_get_channel_by_channel_id,
    db_get_user_by_u_id
)
from .auth import validate_token
from .error import ValueError, AccessError

# Invite user with u_id to channel with channel_id.
# Return {} if successful.
# Raises ValueError exception if channel_id is invalid/user is not in channel or
# if u_id is invalid.
def channel_invite(token, channel_id, receiver_id):
    sender_id = validate_token(token)
    sender = db_get_user_by_u_id(sender_id)

    receiver = db_get_user_by_u_id(receiver_id)
    if receiver is None:
        raise ValueError(description="User with u_id does not exist!")
    channel = db_get_channel_by_channel_id(channel_id)
    if channel is None:
        raise ValueError(description="Channel with channel_id does not exist!")

    if not sender.in_channel(channel):
        raise AccessError(description="Invite sender is not member of channel!")

    channel.add_member(receiver)
    receiver.join_channel(channel)

    return {}

# Given channel with channel_id that user is in, return details about channel.
# Raise ValueError exception if channel with id does not exist.
# Raise AccessError exception if user is not member of channel.
def channel_details(token, channel_id):
    u_id = validate_token(token)
    user = db_get_user_by_u_id(u_id)

    channel = db_get_channel_by_channel_id(channel_id)
    if channel is None:
        raise ValueError(description="Channel with channel_id does not exist!")

    if not user.in_channel(channel):
        raise AccessError(description="User is not member of channel!")

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
    u_id = validate_token(token)
    user = db_get_user_by_u_id(u_id)

    channel = db_get_channel_by_channel_id(channel_id)
    if channel is None:
        raise ValueError(description="Channel with channel_id does not exist!")
    if not user.in_channel(channel):
        raise AccessError(description="User is not member of channel!")
        
    offset = 0
    all_messages = channel.get_messages()
    if (len(all_messages) == 0):
        return {'messages': [], 'start': 0, 'end': -1}
    for message in all_messages:
        if message.get_time_created() > time.time():
            offset += 1
        else:
            break
    if start >= len(all_messages) - offset:
        raise ValueError(description="Start index is greater than the number of messages in the channel!")

    counter = start
    messages = []
    while (counter + offset) < len(all_messages) and counter < start + 50:
        message_dict = {}
        current_message = all_messages[counter + offset]
        message_dict['message_id'] = current_message.get_message_id()
        message_dict['u_id'] = current_message.get_sender().get_u_id()
        message_dict['message'] = current_message.get_text()
        message_dict['time_created'] = current_message.get_time_created()

        message_dict['reacts'] = []
        for react in current_message.get_reacts():
            react_id = react['react_id']
            react_users = react['users']

            react_u_ids = []
            for react_user in react_users:
                react_u_ids.append(react_user.get_u_id())

            reacted = u_id in react_u_ids
            message_dict['reacts'].append({'react_id': react_id, 'u_ids': react_u_ids, 'is_this_user_reacted': reacted})

        message_dict['is_pinned'] = current_message.is_pinned()
        messages.append(message_dict)
        counter += 1
    end = counter - 1
    if end + offset >= len(all_messages):
        end = -1
    return {'messages': messages, 'start': start, 'end': end}

# Given channel ID, remove user from channel. Returns {}.
# Raise ValueError exception if channel with id does not exist.
# An owner leaving removes them from the channel's owner list.
def channel_leave(token, channel_id):
    u_id = validate_token(token)
    user = db_get_user_by_u_id(u_id)

    channel = db_get_channel_by_channel_id(channel_id)
    if channel is None:
        raise ValueError(description="Channel with channel_id does not exist!")

    channel.remove_owner(user)
    channel.remove_member(user)
    user.leave_channel(channel)

    return {}

# Given id of channel that user can join, add them to that channel.
# Raise ValueError exception if channel with id does not exist.
# Raise AccessError if channel is private and user is not admin.
# Raise TokenError if token invalid.
def channel_join(token, channel_id):
    u_id = validate_token(token)
    user = db_get_user_by_u_id(u_id)

    channel = db_get_channel_by_channel_id(channel_id)
    if channel is None:
        raise ValueError(description="Channel with channel_id does not exist!")

    if not channel.is_public():
        if user.get_slackr_role() != Role.admin and user.get_slackr_role() != Role.owner:
            raise AccessError(description="Channel is private and user is not admin or owner!")

    channel.add_member(user)
    user.join_channel(channel)

    return {}

# Make user with u_id an owner of channel. Returns {}.
# Raise ValueError exception if channel with id does not exist or user is
# already owner of channel.
# Raise AccessError exception if user is not owner of either slackr or channel.
def channel_addowner(token, channel_id, target_id):
    u_id = validate_token(token)
    authorised_user = db_get_user_by_u_id(u_id)

    target_user = db_get_user_by_u_id(target_id)

    channel = db_get_channel_by_channel_id(channel_id)
    if channel is None:
        raise ValueError(description="Channel with channel_id does not exist!")
    # user already owner of channel
    if channel.has_true_owner(target_user):
        raise ValueError(description="User already an owner of channel")
    # Authorised u_id not owner of slackr and not owner of channel
    if not channel.has_owner(authorised_user):
        raise AccessError(description="Authorised user is not an owner of the slack or channel")
    
    channel.add_owner(target_user)
    
    return {}

# Remove user with u_id as owner of this channel. Returns {}.
# Raise ValueError exception if channel with id does not exist or user is not
# owner of channel.
# Raise AccessError exception if user is not owner of either slackr or channel.
def channel_removeowner(token, channel_id, target_id):
    u_id = validate_token(token)
    authorised_user = db_get_user_by_u_id(u_id)

    target_user = db_get_user_by_u_id(target_id)

    channel = db_get_channel_by_channel_id(channel_id)
    if channel is None:
        raise ValueError(description="Channel with channel_id does not exist!")
    # user already owner of channel
    if not channel.has_true_owner(target_user):
        raise ValueError(description="User already not an owner of channel")
    # Authorised u_id not owner of slackr and not owner of channel
    if not channel.has_owner(authorised_user):
        raise AccessError(description="Authorised user is not an owner of the slack or channel")
    
    channel.remove_owner(target_user)
    
    return {}

