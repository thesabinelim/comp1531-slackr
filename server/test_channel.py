# COMP1531 Project channel tests
# Written by Sabine Lim z5242579
# 01/10/19

import pytest

from auth import *
from channels import *
from channel import *

########################
# channel_invite Tests #
########################

def test_channel_invite_simple():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    create_dict2 = channels_create(reg_dict2['token'], 'PCSoc', False)
    create_dict3 = channels_create(reg_dict3['token'], 'Steam', True)
    # SETUP END

    # Sabine invites Test to PCSoc
    assert channel_invite(reg_dict2['token'], create_dict2['channel_id'], \
        reg_dict1['u_id']) == {}
    assert channels_list(reg_dict1['token']) == {
        'channels': [
            {3054207, 'PCSoc'},
            {7654321, '1531 autotest'}
        ]
    }

    # Gabe invites Test to Steam
    assert channel_invite(reg_dict3['token'], create_dict3['channel_id'], \
        reg_dict1['u_id']) == {}
    assert channels_list(reg_dict1['token']) == {
        'channels': [
            {3054207, 'PCSoc'},
            {7654321, '1531 autotest'},
            {9703358, 'Steam'}
        ]
    }

    # Check that Sabine and Gabe's channel lists were unmodified
    assert channels_list(reg_dict2['token']) == {
        'channels': [{3054207, 'PCSoc'}]
    }
    assert channels_list(reg_dict3['token']) == {
        {9703358, 'Steam'}
    }

def test_channel_invite_bad_channelid():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    create_dict2 = channels_create(reg_dict2['token'], 'PCSoc', False)
    create_dict3 = channels_create(reg_dict3['token'], 'Steam', True)
    # SETUP END

    

def test_channel_invite_bad_uid():
    pass

def test_channel_invite_notinchannel():
    pass

######################
# channel_join Tests #
######################

def test_channel_join_simple():
    pass
