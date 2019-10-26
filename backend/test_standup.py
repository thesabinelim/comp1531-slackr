# COMP1531 Project standup tests
# Written by Jake Tyler z5208823
# 1/10/19

import pytest
import time
import datetime

from .auth import (
        auth_register, auth_login, auth_logout
)
from .channels import (
        channels_create
)
from .standup import (
        standup_send, standup_start
)
from .db import reset_data, db_add_time_offset, db_reset_time_offset
from .error import ValueError, AccessError


# Helper class to manipulate time for testing standup errors
class TestDateTime:
    # def __init__(self):
    #     self.original_time = datetime.datetime
    # def now_plus_minutes(self, add_minutes):
    #     datetime.datetime = datetime.datetime + datetime.timedelta(minutes=add_minutes)
    # def reset_time(self):
    #     datetime.datetime = self.original_time
    def now(self):
        t = time.time()
        return time.time(t.hour, t.minute+15, t.second, t.microsecond)

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
    assert 'time_finish' in sup_dict1

def test_standup_start_bad_channelid():
    # SETUP BEGIN
    reset_data()
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END

    with pytest.raises(ValueError):
        standup_start(reg_dict1['token'], create_dict1['channel_id'] + 1)

def test_standup_start_notinchannel():
    # SETUP BEGIN
    reset_data()
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
    reset_data()
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END
    
    sup_dict1 = standup_start(reg_dict1['token'], create_dict1['channel_id'])
    assert sup_dict1
    assert 'time_finish' in sup_dict1

    assert standup_send(reg_dict1['token'], create_dict1['channel_id'], 'Hello World') == {}

def test_standup_send_notstarted():
    # SETUP BEGIN
    reset_data()
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END

    with pytest.raises(ValueError):
        standup_send(reg_dict1['token'], create_dict1['channel_id'], 'This shouldn\'t send')

def test_standup_send_notinchannel():
    # SETUP BEGIN
    reset_data()
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END

    with pytest.raises(AccessError):
        standup_send(reg_dict2['token'], create_dict1['channel_id'], 'This shouldn\'t send')

def test_standup_bad_channelid():
    # SETUP BEGIN
    reset_data()
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END
    
    sup_dict1 = standup_start(reg_dict1['token'], create_dict1['channel_id'])
    assert sup_dict1
    assert 'time_finish' in sup_dict1
    
    with pytest.raises(ValueError):
        standup_send(reg_dict1['token'], create_dict1['channel_id'] + 1, 'This shouldn\'t send')

def test_standup_send_toolong():
    # SETUP BEGIN
    reset_data()
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END
    
    sup_dict1 = standup_start(reg_dict1['token'], create_dict1['channel_id'])
    assert sup_dict1
    assert 'time_finish' in sup_dict1
    
    with pytest.raises(ValueError):
        standup_send(reg_dict1['token'], create_dict1['channel_id'], 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')


def test_standup_send_standup_finished():
    # SETUP BEGIN
    reset_data()
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END
    
    sup_dict1 = standup_start(reg_dict1['token'], create_dict1['channel_id'])
    assert sup_dict1
    assert 'time_finish' in sup_dict1
    
    # Standup works
    standup_send(reg_dict1['token'], create_dict1['channel_id'], 'This will send!')
    
    # Artificially say that the time has expired (16 minutes later)
    db_add_time_offset(16 * 60)
    with pytest.raises(ValueError):
        standup_send(reg_dict1['token'], create_dict1['channel_id'], 'This shouldn\'t send')