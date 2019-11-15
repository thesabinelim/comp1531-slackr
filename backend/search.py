# COMP1531 Project search
# Written by Eric Lin z5257305 and Sabine Lim z5242579
# 24/10/19

from .auth import validate_token

from .db import db_get_user_by_u_id
from .channel import channel_messages

# Given a query string, return a collection of messages in a specific channel that match the query
def search_channel(token, channel, query_str):
    results = []
    start = 0
    while start != -1: 
        messages = channel_messages(token, channel.get_channel_id(), start)
        for message in messages['messages']:
            if query_str.lower() in message['message'].lower():
                results.append(message)
        start = messages['end']
    return results

# Given a query string, return a collection of messages that match the query
def search(token, query_str):
    user = validate_token(token)

    channels = user.get_channels()

    results = []
    for channel in channels:
        results.extend(search_channel(token, channel, query_str))
    return {'messages': results}
