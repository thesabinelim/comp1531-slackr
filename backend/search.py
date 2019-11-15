# COMP1531 Project search
# Written by Eric Lin z5257305 and Sabine Lim z5242579
# 24/10/19

from .auth import validate_token

from .db import (
    db_get_user_by_u_id
)
from .channel import (
    channel_messages
)
# Given a query string, return a collection of messages that match the query
def search(token, query_str):
    user = validate_token(token)
    channels = user.get_channels()

    search_messages = []
    for channel in channels:
        start = 0
        match_message = []
        while start != -1: 
            match_message = channel_messages(token, channel.get_channel_id(), start)
            for channel_message in match_message['messages']:
                if query_str.lower() in channel_message['message'].lower():
                    search_messages.append(channel_message)
            start = match_message['end']
    return {'messages': search_messages}
