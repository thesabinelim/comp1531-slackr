# COMP1531 Project channels
# Written by Sabine Lim z5242579
# and Bridget McCarthy z5255505
# 01/10/19

from .db import (
    User, Channel, db_create_channel, db_get_channel_by_channel_id,
    db_get_user_by_u_id, db_get_all_channels
)
from .auth import validate_token

# Return list of channels (and their details) that user is in.
def channels_list(token):
    u_id = validate_token(token)
    user = db_get_user_by_u_id(u_id)

    channels = user.get_channels()
    channel_detail_list = get_channel_list_details(channels)

    return {'channels': channel_detail_list}

# Return list of channels (and their details).
def channels_listall(token):
    validate_token(token)

    channels = db_get_all_channels()
    channel_detail_list = get_channel_list_details(channels)

    return {'channels': channel_detail_list}

# Helper function to return a list of dictionaries containing the channel_id,
# and name of each channel within the supplied 'channel_ids' list.
def get_channel_list_details(channels):
    channel_detail_list = []
    for channel in channels:
        channel_detail_list.append({
            'channel_id': channel.get_channel_id(),
            'name': channel.get_name()
        })
    return channel_detail_list

# Create new channel with that name that is either a public or private channel.
# Return dictionary containing channel_id.
# Raise ValueError exception if name > 20 characters.
# Raise TokenError if token invalid.
def channels_create(token, name, is_public):
    if len(name) > 20:
        raise ValueError("Name longer than 20 characters!")

    u_id = validate_token(token)
    user = db_get_user_by_u_id(u_id)

    channel = db_create_channel(name, is_public)
    channel_id = channel.get_channel_id()

    channel.add_member(user)
    # Make channel creator owner of channel
    channel.add_owner(user)

    return {'channel_id': channel_id}
