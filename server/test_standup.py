# COMP1531 Project standup tests
# Written by Jake Tyler z5208823
# 1/10/19

import pytest

from stand_up import *
from error import *

# So that channels and accounts can be created
from channel import *
from auth import *


#######################
# standup_start Tests #
#######################

# the following tests involve token input and may
# need to be adjusted later

# trying to standup_start a nonexistent channel
def test_standup_start_invalidchannel():
    auth_register('user@example.com', 'validpassword', 'Test', 'User')
    token = authRegisterDict['token']

    with pytest.raises(ValueError):
        standup_start(token, 'Channel Name')

# creating then leaving a channel then testing for being able
# to standup_start that channel.
def test_standup_start_notmember():
    auth_register('user@example.com', 'validpassword', 'Test', 'User')
    token = authRegisterDict['token']
    
    channelsCreateDict = channels_create(token, 'channel name', public)
    channelId = channelsCreateDict['channelId']
    
    channel_leave(token, channelId)
    
    with pytest.raises(AccessError):
        time = standup_start(token, channelId)


#######################
#  standup_send Tests #
#######################

# a standup is running however the user has left so can't add to queue
def test_standup_send_notmember():
    auth_register('user@example.com', 'validpassword', 'Test', 'User')
    token = authRegisterDict['token']
    
    channelsCreateDict = channels_create(token, 'channel name', public)
    channelId = channelsCreateDict['channelId']
    
    time = standup_start(token, channelId)
    channel_leave(token, channelId)
    
    with pytest.raises(AccessError):
        standup_send(token, channelId, 'This should not add')








