# COMP1531 Project channels tests
# Written by Sabine Lim z5242579
# 01/10/19

import pytest

from auth import *
from channels import *
from channel import *

#########################
# channels_create Tests #
#########################

def test_channels_create_simple():
    # SETUP BEGIN
    regDict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    regDict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    regDict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    # SETUP END

    createDict1 = channels_create(regDict1['token'], '1531 autotest', True)
    assert createDict1 and 'channel_id' in createDict1

    createDict2 = channels_create(regDict2['token'], 'PCSoc', False)
    assert createDict2 and 'channel_id' in createDict2
    # Check that creation attempts returned different values
    assert createDict2['channel_id'] != createDict1['channel_id']

    createDict3 = channels_create(regDict3['token'], 'Steam', True)
    assert createDict3 and 'channel_id' in createDict3
    # Check that creation attempts returned different values
    assert createDict3['channel_id'] != createDict2['channel_id']
    assert createDict3['channel_id'] != createDict1['channel_id']

def test_channels_create_badname():
    # SETUP BEGIN
    regDict = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    # SETUP END

    with pytest.raises(ValueError):
        channels_create(regDict['token'], '123456789012345678901', True)

#######################
# channels_list Tests #
#######################

def test_channels_list_simple():
    # SETUP BEGIN
    regDict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    regDict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    regDict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    regDict4 = auth_register('abc@def.com', 'ghijklmnop', 'Qrst', 'Uvwx')

    createDict1 = channels_create(regDict1['token'], '1531 autotest', True)
    createDict2 = channels_create(regDict2['token'], 'PCSoc', False)
    createDict3 = channels_create(regDict3['token'], 'Steam', True)

    channel_join(regDict2['token'], createDict1['channel_id'])
    channel_join(regDict2['token'], createDict3['channel_id'])

    channel_join(regDict3['token'], createDict1['channel_id'])
    # SETUP END

    assert channels_list(regDict1['token']) == {'channels': [{7654321, '1531 autotest'}]}
    assert channels_list(regDict2['token']) == {'channels': [{3054207, 'PCSoc'}, {7654321, '1531 autotest'}, {9703358, 'Steam'}]}
    assert channels_list(regDict3['token']) == {'channels': [{7654321, '1531 autotest'}, {9703358, 'Steam'}]}
    assert channels_list(regDict4['token']) == {'channels': []}

def test_channels_list_nochannels():
    # SETUP BEGIN
    regDict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    regDict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    regDict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    # SETUP END

    assert channels_list(regDict1['token']) == {'channels': []}
    assert channels_list(regDict2['token']) == {'channels': []}
    assert channels_list(regDict3['token']) == {'channels': []}

def test_channels_list_joinednone():
    # SETUP BEGIN
    regDict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    regDict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    regDict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')

    createDict1 = channels_create(regDict1['token'], '1531 autotest', True)
    createDict2 = channels_create(regDict1['token'], 'PCSoc', False)
    createDict3 = channels_create(regDict1['token'], 'Steam', True)
    # SETUP END

    assert channels_list(regDict2['token']) == {'channels': []}
    assert channels_list(regDict3['token']) == {'channels': []}

##########################
# channels_listall Tests #
##########################

def test_channels_listall_simple():
    # SETUP BEGIN
    regDict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    regDict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    regDict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    regDict4 = auth_register('abc@def.com', 'ghijklmnop', 'Qrst', 'Uvwx')

    createDict1 = channels_create(regDict1['token'], '1531 autotest', True)
    createDict2 = channels_create(regDict2['token'], 'PCSoc', False)
    createDict3 = channels_create(regDict3['token'], 'Steam', True)

    channel_join(regDict2['token'], createDict1['channel_id'])
    channel_join(regDict2['token'], createDict3['channel_id'])

    channel_join(regDict3['token'], createDict1['channel_id'])
    # SETUP END

    assert channels_list(regDict1['token']) == {'channels': [{3054207, 'PCSoc'}, {7654321, '1531 autotest'}, {9703358, 'Steam'}]}
    assert channels_list(regDict2['token']) == {'channels': [{3054207, 'PCSoc'}, {7654321, '1531 autotest'}, {9703358, 'Steam'}]}
    assert channels_list(regDict3['token']) == {'channels': [{3054207, 'PCSoc'}, {7654321, '1531 autotest'}, {9703358, 'Steam'}]}
    assert channels_list(regDict4['token']) == {'channels': [{3054207, 'PCSoc'}, {7654321, '1531 autotest'}, {9703358, 'Steam'}]}

def test_channels_listall_nochannels():
    # SETUP BEGIN
    regDict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    regDict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    regDict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    # SETUP END

    assert channels_list(regDict1['token']) == {'channels': []}
    assert channels_list(regDict2['token']) == {'channels': []}
    assert channels_list(regDict3['token']) == {'channels': []}

def test_channels_listall_createdjoinednone():
    # SETUP BEGIN
    regDict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    regDict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    regDict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')

    createDict1 = channels_create(regDict1['token'], '1531 autotest', True)
    createDict2 = channels_create(regDict1['token'], 'PCSoc', False)
    createDict3 = channels_create(regDict1['token'], 'Steam', True)
    # SETUP END

    assert channels_list(regDict2['token']) == {'channels': [{3054207, 'PCSoc'}, {7654321, '1531 autotest'}, {9703358, 'Steam'}]}
    assert channels_list(regDict3['token']) == {'channels': [{3054207, 'PCSoc'}, {7654321, '1531 autotest'}, {9703358, 'Steam'}]}
