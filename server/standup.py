# COMP1531 Project standup stubs
# Written by Jake Tyler z5208823
# 3/10/19

from channel import *
from auth import *
from error import *

# standup_start commands initiates 15 minutes of standup and then returns
# 15 minutes of stand up time. It returns a ValueError when the channel_id
# is invalid, as in the channel doesnt exist and returns an AccessError
# when the channel exists but the user isnt in that channel.
def standup_start(token, channel_id):
    
    if channel_id == 'invalid':
        raise ValueError
    
    if channel_list(token) != channel_id:
        raise AccessError

    timeLeft = 15
    return timeLeft

# The standup_send function takes the users token, the desired channel_id
# and a message under 1000 characters and puts it in the standup_queue.
# A ValueError is raised when the channel_id is invalid in the case of the
# channel not existing and if the message is too long. An AccessError is
# raised when the user is not part of the channel and when the time
# left in the stand is 0, ie if the stand is no longer in place.
def standup_send(token, channel_id, message):
    
    if channel_id == 'invalid':
        raise ValueError
    
    if len(message) > 1000:
        raise ValueError

    if channel_list(token) != channel_id:
        raise AccessError

    if timeLeft <= 0:
        raise AccessError
    
    pass
