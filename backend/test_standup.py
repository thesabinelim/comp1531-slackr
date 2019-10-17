# COMP1531 Project standup tests
# Written by Jake Tyler z5208823
# 1/10/19

import pytest

from auth import *
from channel import *
from channels import *
from standup import *
from error import *

#######################
# standup_start Tests #
#######################

def test_standup_start_simple():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END
    
    sup_dict1 = standup_start(reg_dict1['token'], create_dict1['channel_id'])
    assert sup_dict1
    assert 'time_finish' in sup_dict1

def test_standup_start_bad_channelid():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END

    with pytest.raises(ValueError):
        standup_start(reg_dict1['token'], create_dict1['channel_id'] + 1)

def test_standup_start_notinchannel():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END

    with pytest.raises(AccessError):
        standup_start(reg_dict2['token'], create_dict1['channel_id'])

######################
# standup_send Tests #
######################

def test_standup_send_simple():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END
    
    sup_dict1 = standup_start(reg_dict1['token'], create_dict1['channel_id'])
    assert sup_dict1
    assert 'time_finish' in sup_dict1

    assert standup_send(reg_dict1['token'], create_dict1['channel_id'], 'Hello World') == {}

def test_standup_send_notstarted():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END

    with pytest.raises(AccessError):
        standup_send(reg_dict1['token'], create_dict1['channel_id'], 'This shouldn\'t send')

def test_standup_send_notinchannel():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END

    with pytest.raises(AccessError):
        standup_send(reg_dict2['token'], create_dict1['channel_id'], 'This shouldn\'t send')

def test_standup_bad_channelid():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END
    
    sup_dict1 = standup_start(reg_dict1['token'], create_dict1['channel_id'])
    assert sup_dict1
    assert 'time_finish' in sup_dict1
    
    with pytest.raises(ValueError):
        standup_send(reg_dict1['token'], create_dict1['channel_id'], 'This shouldn\'t send')

def test_standup_send_toolong():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END
    
    sup_dict1 = standup_start(reg_dict1['token'], create_dict1['channel_id'])
    assert sup_dict1
    assert 'time_finish' in sup_dict1
    
    with pytest.raises(ValueError):
        standup_send(reg_dict1['token'], create_dict1['channel_id'], 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
