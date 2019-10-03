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

# trying to standup_start a nonexistent channel should return a ValueError
def test_standup_start_invalidchannel():
    auth_register('user@example.com', 'validpassword', 'Test', 'User')
    token = authRegisterDict['token']

    with pytest.raises(ValueError):
        standup_start(token, 'Channel Name')

# creating then leaving a channel then testing for being able
# to standup_start that channel. This should return an AccessError.
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

# a standup is running however the user has left the channel so doesn't
# have permission to add to queue should return a AccessError
def test_standup_send_notmember():
    auth_register('user@example.com', 'validpassword', 'Test', 'User')
    token = authRegisterDict['token']
    
    channelsCreateDict = channels_create(token, 'channel name', public)
    channelId = channelsCreateDict['channelId']
    
    time = standup_start(token, channelId)
    channel_leave(token, channelId)
    
    with pytest.raises(AccessError):
        standup_send(token, channelId, 'This should not add')

# tests that when the channel doesn't exist that a ValueError returns
def test_standup_send_nochannel():
    auth_register('user@example.com', 'validpassword', 'Test', 'User')
    token = authRegisterDict['token']
    
    with pytest.raises(ValueError):
        standup_send(token, channelId, 'This should not add')

# tests that when the standup_time is 0 a ValueError is returned
def test_standup_send_time():
    auth_register('user@example.com', 'validpassword', 'Test', 'User')
    token = authRegisterDict['token']
    
    channelsCreateDict = channels_create(token, 'channel name', public)
    channelId = channelsCreateDict['channelId']
    
    time = standup_start(token, channelId)
    time = 0
    
    with pytest.raises(ValueError):
        standup_send(token, channelId, 'This should not add')

# tests that when the length of the string is over 1000 characters a
# ValueError is returned
def test_standup_send_length():
    auth_register('user@example.com', 'validpassword', 'Test', 'User')
    token = authRegisterDict['token']
    
    channelsCreateDict = channels_create(token, 'channel name', public)
    channelId = channelsCreateDict['channelId']
    
    time = standup_start(token, channelId)
    
    with pytest.raises(ValueError):
        standup_send(token, channelId, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')





