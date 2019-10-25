# COMP1531 Project search
# Written by Eric Lin z5257305 and Sabine Lim z5242579
# 24/10/19

import re

# Given a query string, return a collection of messages that match the query
def search(token, query_str):
    u_id = validate_token(token)
    user = db_get_user_by_u_id(u_id)

    query_re = re.compile(f'{query_str.lower()}')
    channels = user.get_channels()

    match_messages = []
    for channel in channels:
        start = 0
        while start != -1: 
            channel_messages = channel_messages(token, channel, start)
            for channel_message in channel_messages['messages']:
                if query_re.match(message['message']):
                    search_messages.append(channel_message)
            start = channel_messages['end']
    return {'messages': search_messages}
