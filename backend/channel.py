# COMP1531 Project channel
# Written by Sabine Lim z5242579, Bridget McCarthy z5255505
# and Eric Lin z5257305
# 23/10/19

from time import time

from .db import (
    Role, User, Channel, Message, db_get_channel_by_channel_id,
    db_get_user_by_u_id, db_get_time_offset
)
from .auth import validate_token
from .error import ValueError, AccessError

############################## Channel Setup ########################################

def channel_setup_notarget(token, channel_id):
    
    # sets up the sender and channel
    sender = validate_token(token)
    channel = db_get_channel_by_channel_id(channel_id)
    
    return sender, channel

def channel_setup_target(token, channel_id, receiver_id):

    # sets up the sender, channel and reciever
    sender = validate_token(token)
    channel = db_get_channel_by_channel_id(channel_id)
    receiver = db_get_user_by_u_id(receiver_id)
    
    return sender, channel, receiver

############################# Channel Invite #######################################

# Invite user with u_id to channel with channel_id.
# Return {} if successful.
# Raises ValueError exception if channel_id is invalid/user is not in channel or
# if u_id is invalid.

def channel_invite(token, channel_id, receiver_id):
    
    # authenticates the user and channel
    sender, channel, receiver = channel_setup_target(token, channel_id, receiver_id)
    
    # checks for errors
    channel_invite_error(sender, channel, receiver)

    # adds the member
    channel.add_member(receiver)
    receiver.join_channel(channel)

    return {}

# any errors possible, passing in all values.
def channel_invite_error(sender, channel, receiver):
    
    if not sender.in_channel(channel):
        raise AccessError(description = "Invite sender is not member of channel!")

############################# Channel Details #######################################

# Given channel with channel_id that user is in, return details about channel.
# Raise ValueError exception if channel with id does not exist.
# Raise AccessError exception if user is not member of channel.

def channel_details(token, channel_id):
    
    sender, channel = channel_setup_notarget(token, channel_id)
    channel_details_error(sender, channel)

    name = channel.get_name()
    owner_members = []
    for owner in channel.get_owners():
        owner_members.append(owner.to_dict_short())

    all_members = []
    for member in channel.get_members():
        all_members.append(member.to_dict_short())

    return {
        'name': name,
        'owner_members': owner_members,
        'all_members': all_members
    }

def channel_details_error(sender, channel):

    if not sender.in_channel(channel):
        raise AccessError(description = "User is not member of channel!")

############################# Channel Messages #######################################

# Given channel with channel_id that user is in, return up to 50 messages
# between index "start" and "start + 50". Message with index 0 is most recent
# message in channel. Return a new index "end" which is value of "start + 50" or
# if this function returned least recent messages in channel, return -1 in "end"
# to indicate there are no more messages to load after this return.
# Raise ValueError exception when channel with id does not exist or start is >
# total number of messages in channel.
# Raise AccessError exception when user is not member of channel with id.

# main, more documentation to explain general process
def channel_messages(token, channel_id, start):
    
    # sets up the channel
    sender, channel = channel_setup_notarget(token, channel_id)

    # list of all_messages
    all_messages = channel.get_messages()
    
    # Itterates through all messages till correct timeframe
    offset = channel_messages_count(channel, all_messages)
    
    # checks errors
    channel_messages_error(sender, channel, all_messages, offset, start)

    # puts all messages into a list
    messages, end = channel_messages_accumulate(start, offset, all_messages)
    
    return {'messages': messages, 'start': start, 'end': end}

# iterates through the list
def channel_messages_count(channel, all_messages):

    offset = 0
    
    for message in all_messages:
        if message.get_time_created() > time() + db_get_time_offset():
            offset += 1
        else:
            break

    return offset

# accumulates all messages into a list
def channel_messages_accumulate(start, offset, all_messages):

    counter = start
    messages = []
    
    while (counter + offset) < len(all_messages) and counter < start + 50:
        current_message = all_messages[counter + offset]
        messages.append(current_message.to_dict())
        counter += 1
    end = counter
    if end + offset >= len(all_messages):
        end = -1

    return messages, end

# error list
def channel_messages_error(sender, channel, all_messages, offset, start):

    if not sender.in_channel(channel):
        raise AccessError(description = "User is not member of channel!")

    if start != 0 and start >= len(all_messages) - offset:
        raise ValueError(description = "Start index is greater than the number of messages in the channel!")
    
    if (len(all_messages) == 0):
        return {'messages': [], 'start': 0, 'end': -1}

############################# Channel Leave #######################################

# Given channel ID, remove user from channel. Returns {}.
# Raise ValueError exception if channel with id does not exist.
# An owner leaving removes them from the channel's owner list.

def channel_leave(token, channel_id):
    
    sender, channel = channel_setup_notarget(token, channel_id)
    channel_leave_error(sender, channel)
    
    channel.remove_owner(sender)
    channel.remove_member(sender)
    sender.leave_channel(channel)

    return {}

# error list
def channel_leave_error(sender, channel):
    
    # Last owner can't leave unless they are also last member
    if len(channel.get_true_owners()) == 1 and channel.has_true_owner(sender) \
        and len(channel.get_members()) > 1:
        raise ValueError(description = "Last owner cannot leave a channel with members still in it!")

############################# Channel Join ########################################

# Given id of channel that user can join, add them to that channel.
# Raise ValueError exception if channel with id does not exist.
# Raise AccessError if channel is private and user is not admin.
# Raise TokenError if token invalid.

def channel_join(token, channel_id):
    
    sender, channel = channel_setup_notarget(token, channel_id)
    channel_join_error(sender, channel)

    channel.add_member(sender)
    sender.join_channel(channel)

    return {}

def channel_join_error(sender, channel):

    if channel is None:
        raise ValueError(description = "Channel with channel_id does not exist!")

    if not channel.is_public():
        if sender.get_slackr_role() != Role.admin and sender.get_slackr_role() != Role.owner:
            raise AccessError(description = "Channel is private and user is not admin or owner!")

############################# Channel Addowner ########################################

# Make user with u_id an owner of channel. Returns {}.
# Raise ValueError exception if channel with id does not exist or user is
# already owner of channel.
# Raise AccessError exception if user is not owner of either slackr or channel.

def channel_addowner(token, channel_id, target_id):
    authorised_user = validate_token(token)
    
    target_user = db_get_user_by_u_id(target_id)
    
    channel = db_get_channel_by_channel_id(channel_id)
    # user already owner of channel
    if channel.has_true_owner(target_user):
        raise ValueError(description="User already an owner of channel")
    # Authorised u_id not owner of slackr and not owner of channel
    if not channel.has_owner(authorised_user):
        raise AccessError(description="Authorised user is not an owner of the slack or channel")
    
    if not channel.has_member(target_user):
        channel.add_member(target_user)
        target_user.join_channel(channel)
    channel.add_owner(target_user)
    
    return {}

# Remove user with u_id as owner of this channel. Returns {}.
# Raise ValueError exception if channel with id does not exist or user is not
# owner of channel.
# Raise AccessError exception if user is not owner of either slackr or channel.
def channel_removeowner(token, channel_id, target_id):
    authorised_user = validate_token(token)
    
    target_user = db_get_user_by_u_id(target_id)
    
    channel = db_get_channel_by_channel_id(channel_id)
    # user already owner of channel
    if not channel.has_true_owner(target_user):
        raise ValueError(description="User already not an owner of channel")
    # Authorised u_id not owner of slackr and not owner of channel
    if not channel.has_owner(authorised_user):
        raise AccessError(description="Authorised user is not an owner of the slack or channel")
    
    channel.remove_owner(target_user)
    
    return {}
