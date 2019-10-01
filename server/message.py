# COMP1531 Project message
# Written by Bridget McCarthy z5255505
# 1/10/19

# Send a message from authorised_user to the channel specified by channel_id.
# automatically at a specified time in the future. 
# Raises ValueError exception when channel_id doesn't exist, messige is more
# than 1000 characters, or time_sent is a past time.
# No return value.
def message_sendlater(token, channel_id, message, time_sent):
    pass

# Send a message from authorised_user to the channel specified by channel_id.
# Raises ValueError exception when the message is more than 1000 characters.
# No return value.
def message_send(token, channel_id, message):
    # Can't exactly test token stuff right now
    if message.length() > 1000:
        raise ValueError

    # An assumption I'm making is that the channel_id has to be valid, like in
    # send_later
    # if channel_id is invalid
    #   raise ValueError

# Given a message_id for a message, this message is removed from the channel.
# Raises ValueError when the message_id no longer exists.
# No return value.
def message_remove(token, message_id):
    pass

# Given a message, update it's text with new text. No return value.
def message_edit(token, message_id, message):
    pass

# Given a message within a channel the authorised user is part of, add a "react"
# to that particular message. No return value.
def message_react(token, message_id, react_id):
    pass

# Given a message within a channel the authorised user is part of, remove a 
# "react" to that particular message. No return value.
def message_unreact(token, message_id, react_id):
    pass

# Given a message within a channel, mark it as "pinned" to be given special 
# display treatment by the frontend. No return value.
def message_pin(token, message_id):
    pass

# Given a message within a channel, remove it's mark as unpinned. No return 
# value.
def message_unpin(token, message_id):
    pass
