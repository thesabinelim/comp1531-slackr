# COMP1531 Project channels
# Written by Sabine Lim z5242579
# and Bridget McCarthy z5255505
# 01/10/19

from .db import (
    User, Channel, db_create_channel, db_get_channel_by_channel_id,
    db_get_user_by_u_id, db_get_all_channels
)
from .auth import validate_token
from .error import ValueError

############################## Channels List ########################################

# Return list of channels (and their details) that user is in.

def channels_list(token):
    user = validate_token(token)

    channel_detail_list = get_channel_list_details(user.get_channels())

    return {'channels': channel_detail_list}

############################## Channels Listall #####################################

# Return list of channels (and their details).

def channels_listall(token):
    validate_token(token)

    channel_detail_list = get_channel_list_details(db_get_all_channels())

    return {'channels': channel_detail_list}

############################## Get Channel list ######################################

# Helper function to return a list of dictionaries containing the channel_id,
# and name of each channel within the supplied 'channel_ids' list.

def get_channel_list_details(channels):
    channel_detail_list = []
    for channel in channels:
        channel_detail_list.append(channel.to_dict())
    return channel_detail_list

############################## Channels Create ########################################

# Create new channel with that name that is either a public or private channel.
# Return dictionary containing channel_id.
# Raise ValueError exception if name > 20 characters.

def channels_create(token, name, is_public):
    
    channels_create_error(name)
    user = validate_token(token)

    channel = db_create_channel(name, is_public)
    channel_id = channel.get_channel_id()

    # Adds user and makes user owner of the channel
    channel.add_member(user)
    channel.add_owner(user)
    user.join_channel(channel)

    return {'channel_id': channel_id}

# error list
def channels_create_error(name):
    
    if len(name) > 20:
        raise ValueError(description = "Name longer than 20 characters!")
