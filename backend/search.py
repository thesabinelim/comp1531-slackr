# COMP1531 Project search
# Written by Eric Lin z5257305 and Sabine Lim z5242579
# 24/10/19

import re

from .auth import validate_token

from .db import (
    db_get_user_by_u_id
)
from .channel import (
    channel_messages
)
# Given a query string, return a collection of messages that match the query
def search(token, query_str):
    u_id = validate_token(token)
    user = db_get_user_by_u_id(u_id)

    query_re = re.compile(f'{query_str.lower()}')
    channels = user.get_channels()

    search_messages = []
    for channel in channels:
        start = 0
        match_message = []
        while start != -1: 
            match_message = channel_messages(token, channel, start)
            for channel_message in match_message['messages']:
                if query_re.match(channel_message['message']):
                    search_messages.append(channel_message)
            start = match_message['end']
    return {'messages': search_messages}
