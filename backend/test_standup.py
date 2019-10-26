# COMP1531 Project standup tests
# Written by Jake Tyler z5208823
# and Bridget McCarthy z5255505
# 1/10/19

import pytest
import time
import datetime

from .auth import (
        auth_register, auth_login, auth_logout
)
from .channel import channel_join
from .channels import (
        channels_create
)
from .standup import (
        standup_send, standup_start
)
from .db import reset_data, db_add_time_offset, db_reset_time_offset, db_get_channel_by_channel_id
from .error import ValueError, AccessError

#######################
# standup_start Tests #
#######################

def test_standup_start_simple():
    # SETUP BEGIN
    reset_data()
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END
    
    sup_dict1 = standup_start(reg_dict1['token'], create_dict1['channel_id'])
    assert sup_dict1
    assert sup_dict1['time_finish'] >= time.time() + 15 * 60 - 1

    channel = db_get_channel_by_channel_id(create_dict1['channel_id'])
    assert channel.get_standup().get_text() == ""

def test_standup_start_already_running():
    # SETUP BEGIN
    reset_data()
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END
    
    sup_dict1 = standup_start(reg_dict1['token'], create_dict1['channel_id'])
    assert sup_dict1
    assert sup_dict1['time_finish'] >= time.time() + 15 * 60 - 1

    with pytest.raises(ValueError):
        standup_start(reg_dict1['token'], create_dict1['channel_id'])
    
    channel = db_get_channel_by_channel_id(create_dict1['channel_id'])
    assert channel.get_standup().get_text() == ""
    
def test_standup_start_bad_channelid():
    # SETUP BEGIN
    reset_data()
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END

    with pytest.raises(ValueError):
        standup_start(reg_dict1['token'], create_dict1['channel_id'] + 1)

    channel = db_get_channel_by_channel_id(create_dict1['channel_id'])
    assert channel.get_standup() is None

def test_standup_start_notinchannel():
    # SETUP BEGIN
    reset_data()
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END

    with pytest.raises(AccessError):
        standup_start(reg_dict2['token'], create_dict1['channel_id'])
    
    channel = db_get_channel_by_channel_id(create_dict1['channel_id'])
    assert channel.get_standup() is None

######################
# standup_send Tests #
######################

def test_standup_send_simple():
    # SETUP BEGIN
    reset_data()
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END
    
    sup_dict1 = standup_start(reg_dict1['token'], create_dict1['channel_id'])
    assert sup_dict1
    assert sup_dict1['time_finish'] >= time.time() + 15 * 60 - 1

    assert standup_send(reg_dict1['token'], create_dict1['channel_id'], 'Hello World') == {}
    channel = db_get_channel_by_channel_id(create_dict1['channel_id'])
    assert channel.get_standup().get_text() == f"testuser: Hello World \n"

def test_standup_send_notstarted():
    # SETUP BEGIN
    reset_data()
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END

    with pytest.raises(ValueError):
        standup_send(reg_dict1['token'], create_dict1['channel_id'], 'This shouldn\'t send')
    channel = db_get_channel_by_channel_id(create_dict1['channel_id'])
    assert channel.get_standup() is None

def test_standup_send_notinchannel():
    # SETUP BEGIN
    reset_data()
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END

    with pytest.raises(AccessError):
        standup_send(reg_dict2['token'], create_dict1['channel_id'], 'This shouldn\'t send')
    channel = db_get_channel_by_channel_id(create_dict1['channel_id'])
    assert channel.get_standup() is None

def test_standup_bad_channelid():
    # SETUP BEGIN
    reset_data()
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END
    
    sup_dict1 = standup_start(reg_dict1['token'], create_dict1['channel_id'])
    assert sup_dict1
    assert sup_dict1['time_finish'] >= time.time() + 15 * 60 - 1
    
    with pytest.raises(ValueError):
        standup_send(reg_dict1['token'], create_dict1['channel_id'] + 1, 'This shouldn\'t send')
    channel = db_get_channel_by_channel_id(create_dict1['channel_id'])
    assert channel.get_standup().get_text() == f""

def test_standup_send_toolong():
    # SETUP BEGIN
    reset_data()
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END
    
    sup_dict1 = standup_start(reg_dict1['token'], create_dict1['channel_id'])
    assert sup_dict1
    assert sup_dict1['time_finish'] >= time.time() + 15 * 60 - 1
    
    with pytest.raises(ValueError):
        standup_send(reg_dict1['token'], create_dict1['channel_id'], 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    channel = db_get_channel_by_channel_id(create_dict1['channel_id'])
    assert channel.get_standup().get_text() == f""

def test_standup_send_standup_finished():
    # SETUP BEGIN
    reset_data()
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], create_dict1['channel_id'])
    # SETUP END
    
    sup_dict1 = standup_start(reg_dict1['token'], create_dict1['channel_id'])
    assert sup_dict1
    assert sup_dict1['time_finish'] >= time.time() + 15 * 60 - 1
    
    # Standup works
    channel = db_get_channel_by_channel_id(create_dict1['channel_id'])
    standup_send(reg_dict1['token'], create_dict1['channel_id'], 'This will send!')
    assert channel.get_standup().get_text() == f"testuser: This will send! \n"

    standup_send(reg_dict2['token'], create_dict1['channel_id'], 'bazinga')
    assert channel.get_standup().get_text() == f"testuser: This will send! \nsabinelim: bazinga \n"

    # Still within timeframe, so another user can send
    # Artificially say that the time has expired (16 minutes later)
    db_add_time_offset(16 * 60)
    with pytest.raises(ValueError):
        standup_send(reg_dict1['token'], create_dict1['channel_id'], 'This shouldn\'t send')
    