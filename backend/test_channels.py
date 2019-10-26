# COMP1531 Project channels tests
# Written by Sabine Lim z5242579
# 01/10/19

import pytest

from .db import reset_data
from .auth import auth_register
from .channels import channels_create, channels_list, channels_listall
from .channel import channel_join
from .error import ValueError, AccessError

#########################
# channels_create Tests #
#########################

def test_channels_create_simple():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    # SETUP END

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    create_dict2 = channels_create(reg_dict2['token'], 'PCSoc', False)
    create_dict3 = channels_create(reg_dict3['token'], 'Steam', True)

    # Check that creation attempts returned different values
    assert create_dict1['channel_id'] != create_dict2['channel_id'] != create_dict3['channel_id']

def test_channels_create_same_name():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    # SETUP END

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    create_dict2 = channels_create(reg_dict1['token'], '1531 autotest', True)

    # Check that creation attempts returned different values
    assert create_dict1['channel_id'] != create_dict2['channel_id']

def test_channels_create_name_too_long():
    # SETUP BEGIN
    reset_data()

    reg_dict = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    # SETUP END

    with pytest.raises(ValueError):
        channels_create(reg_dict['token'], 'longnameisover20chars', True)

#######################
# channels_list Tests #
#######################

def test_channels_list_simple():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    reg_dict4 = auth_register('abc@def.com', 'ghijklmnop', 'Qrst', 'Uvwx')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    create_dict2 = channels_create(reg_dict2['token'], 'PCSoc', False)
    create_dict3 = channels_create(reg_dict3['token'], 'Steam', True)

    channel_join(reg_dict2['token'], create_dict1['channel_id'])
    channel_join(reg_dict2['token'], create_dict3['channel_id'])

    channel_join(reg_dict3['token'], create_dict1['channel_id'])
    # SETUP END

    # Check that Test is in 1531 autotest
    assert channels_list(reg_dict1['token']) == {
        'channels': [
            {7654321, '1531 autotest'}
        ]
    }

    # Check that Sabine is in PCSoc, 1531 autotest and Steam
    assert channels_list(reg_dict2['token']) == {
        'channels': [
            {3054207, 'PCSoc'},
            {7654321, '1531 autotest'},
            {9703358, 'Steam'}
        ]
    }

    # Check that Gabe is in 1531 autotest and Steam
    assert channels_list(reg_dict3['token']) == {
        'channels': [
            {7654321, '1531 autotest'},
            {9703358, 'Steam'}
        ]
    }

    # Check that Qrst is not in any channels
    assert channels_list(reg_dict4['token']) == {'channels': []}

def test_channels_list_nochannels():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    # SETUP END

    assert channels_list(reg_dict1['token']) == {'channels': []}
    assert channels_list(reg_dict2['token']) == {'channels': []}
    assert channels_list(reg_dict3['token']) == {'channels': []}

def test_channels_list_joinednone():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    create_dict2 = channels_create(reg_dict1['token'], 'PCSoc', False)
    create_dict3 = channels_create(reg_dict1['token'], 'Steam', True)
    # SETUP END

    assert channels_list(reg_dict2['token']) == {'channels': []}
    assert channels_list(reg_dict3['token']) == {'channels': []}

##########################
# channels_listall Tests #
##########################

def test_channels_listall_simple():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    reg_dict4 = auth_register('abc@def.com', 'ghijklmnop', 'Qrst', 'Uvwx')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    create_dict2 = channels_create(reg_dict2['token'], 'PCSoc', False)
    create_dict3 = channels_create(reg_dict3['token'], 'Steam', True)

    channel_join(reg_dict2['token'], create_dict1['channel_id'])
    channel_join(reg_dict2['token'], create_dict3['channel_id'])

    channel_join(reg_dict3['token'], create_dict1['channel_id'])
    # SETUP END

    # Check that all channels are listed for Test, who is in 1 channel
    assert channels_list(reg_dict1['token']) == {
        'channels': [
            {3054207, 'PCSoc'},
            {7654321, '1531 autotest'},
            {9703358, 'Steam'}
        ]
    }

    # Check that all channels are listed for Sabine, who is in all 3 channels
    assert channels_list(reg_dict2['token']) == {
        'channels': [
            {3054207, 'PCSoc'},
            {7654321, '1531 autotest'},
            {9703358, 'Steam'}
        ]
    }

    # Check that all channels are listed for Gabe, who is in 2 channels
    assert channels_list(reg_dict3['token']) == {
        'channels': [
            {3054207, 'PCSoc'},
            {7654321, '1531 autotest'},
            {9703358, 'Steam'}
        ]
    }

    # Check that all channels are listed for Qrst, who is in no channels
    assert channels_list(reg_dict4['token']) == {
        'channels': [
            {3054207, 'PCSoc'},
            {7654321, '1531 autotest'},
            {9703358, 'Steam'}
        ]
    }

def test_channels_listall_nochannels():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    # SETUP END

    assert channels_list(reg_dict1['token']) == {'channels': []}
    assert channels_list(reg_dict2['token']) == {'channels': []}
    assert channels_list(reg_dict3['token']) == {'channels': []}

def test_channels_listall_createdjoinednone():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    create_dict2 = channels_create(reg_dict1['token'], 'PCSoc', False)
    create_dict3 = channels_create(reg_dict1['token'], 'Steam', True)
    # SETUP END

    # Check that all channels are listed for Sabine, who is in no channels
    assert channels_list(reg_dict2['token']) == {
        'channels': [
            {3054207, 'PCSoc'},
            {7654321, '1531 autotest'},
            {9703358, 'Steam'}
        ]
    }

    # Check that all channels are listed for Qrst, who is in no channels
    assert channels_list(reg_dict3['token']) == {
        'channels': [
            {3054207, 'PCSoc'},
            {7654321, '1531 autotest'},
            {9703358, 'Steam'}
        ]
    }
