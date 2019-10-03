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

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END

    with pytest.raises(ValueError):
        assert channel_invite(reg_dict1['token'], create_dict1['channel_id'] + 1, \
            reg_dict1['u_id']) == {}

def test_channel_invite_bad_uid():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END

    u_id = reg_dict2['u_id'] + 1
    if (u_id) == reg_dict1['u_id']:
        u_id += 1

    with pytest.raises(ValueError):
        channel_invite(reg_dict1['token'], create_dict1['channel_id'], u_id)

def test_channel_invite_bad_ids():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END

    u_id = reg_dict2['u_id'] + 1
    if (u_id) == reg_dict1['u_id']:
        u_id += 1

    with pytest.raises(ValueError):
        channel_invite(reg_dict1['token'], create_dict1['channel_id'] + 1, u_id)

def test_channel_invite_notinchannel():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    create_dict1 = channels_create(reg_dict2['token'], '1531 autotest', True)
    # SETUP END

    with pytest.raises(ValueError):
        channel_invite(reg_dict1['token'], create_dict1['channel_id'], reg_dict2['u_id'])

def test_channel_invite_allerrors():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    create_dict1 = channels_create(reg_dict2['token'], '1531 autotest', True)
    # SETUP END

    u_id = reg_dict2['u_id'] + 1
    if (u_id) == reg_dict1['u_id']:
        u_id += 1

    with pytest.raises(ValueError):
        channel_invite(reg_dict1['token'], create_dict1['channel_id'] + 1, u_id)

######################
# channel_join Tests #
######################

def test_channel_join_simple():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    reg_dict4 = auth_register('abc@def.com', 'ghijklmnop', 'Qrst', 'Uvwx')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    create_dict2 = channels_create(reg_dict2['token'], 'PCSoc', False)
    create_dict3 = channels_create(reg_dict3['token'], 'Steam', True)
    # SETUP END

    # Sabine joins 1531 autotest and Steam
    assert channel_join(reg_dict2['token'], create_dict1['channel_id']) == {}

    # Gabe joins 1531 autotest
    assert channel_invite(reg_dict3['token'], create_dict1['channel_id']) == {}

    # Qrst joins 1531 autotest
    assert channel_join(reg_dict4['token'], create_dict1['channel_id']) == {}

    # Check that Test's channel list was unmodified
    assert channels_list(reg_dict1['token']) == {
        'channels': [{7654321, '1531 autotest'}]
    }

    # Check Sabine's channel list
    assert channels_list(reg_dict2['token']) == {
        'channels': [
            {3054207, 'PCSoc'},
            {7654321, '1531 autotest'},
            {9703358, 'Steam'}
        ]
    }

    # Check Gabe's channel list
    assert channels_list(reg_dict3['token']) == {
        'channels': [
            {7654321, '1531 autotest'},
            {9703358, 'Steam'}
        ]
    }

    # Check Qrst's channel list
    assert channels_list(reg_dict4['token']) == {
        'channels': [
            {7654321, '1531 autotest'}
        ]
    }

def test_channel_join_bad_channelid():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END

    with pytest.raises(ValueError):
        channel_join(reg_dict2['token'], create_dict1['channel_id'] + 1)

def test_channel_join_noperms():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    create_dict1 = channels_create(reg_dict1['token'], 'PCSoc', False)
    # SETUP END

    with pytest.raises(AccessError):
        channel_join(reg_dict2['token'], create_dict1['channel_id'])
