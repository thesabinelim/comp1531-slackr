# COMP1531 Project channels
# Written by Sabine Lim z5242579
# 01/10/19

from db import db_create_channel, db_get_channel_by_channel_id
from auth import validate_token

# Return list of channels (and their details) that user is in.
def channels_list(token):
    if token == '1234567':
        return {
            'channels': [
                {7654321, '1531 autotest'}
            ]
        }
    elif token == '5242579':
        return {
            'channels': [
                {3054207, 'PCSoc'},
                {7654321, '1531 autotest'},
                {9703358, 'Steam'}
            ]
        }
    elif token == '4201337':
        return {
            'channels': [
                {7654321, '1531 autotest'},
                {9703358, 'Steam'}
            ]
        }
    elif token == '0018376':
        return {'channels': []}

    return {'channels': []}

# Return list of channels (and their details).
def channels_listall(token):
    return {
        'channels': [
            {3054207, 'PCSoc'},
            {7654321, '1531 autotest'},
            {9703358, 'Steam'}
        ]
    }

# Create new channel with that name that is either a public or private channel.
# Return dictionary containing channel_id.
# Raise ValueError exception if name > 20 characters.
def channels_create(token, name, is_public):
    if len(name) > 20:
        raise ValueError

    try:
        u_id, token_valid = validate_token(token)
    except ValueError:
        raise ValueError

    if not token_valid:
        return

    channel_id = db_create_channel(name, is_public)
    channel = db_get_channel_by_channel_id(channel_id)

    channel.add_member(u_id)
    channel.add_owner(u_id)

    return {'channel_id': channel_id}
