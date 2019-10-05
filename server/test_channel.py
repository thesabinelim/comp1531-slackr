# COMP1531 Project channel tests
# Written by Sabine Lim z5242579
# 01/10/19

import pytest

from auth import *
from channels import *
from channel import *
from error import *

########################
# channel_invite Tests #
########################

def test_channel_invite_simple():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    create_dict2 = channels_create(reg_dict2['token'], 'PCSoc', True)
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

def test_channel_join_no_autoowner():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict2['token'], 'PCSoc', False)
    # SETUP END

    # Sabine invites Test to PCSoc, check that Test not automatically owner of PCSoc
    assert channel_invite(reg_dict2['token'], create_dict1['channel_id'], \
        reg_dict1['u_id']) == {}
    assert {
        'u_id': reg_dict1['u_id'],
        'name_first': 'Test',
        'name_last': 'User'
    } not in channel_details(reg_dict1['token'], create_dict1['channel_id'])['owner_members']

def test_channel_invite_private():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict2['token'], 'PCSoc', False)
    # SETUP END

    # Sabine invites Test to PCSoc
    assert channel_invite(reg_dict2['token'], create_dict1['channel_id'], \
        reg_dict1['u_id']) == {}
    assert channels_list(reg_dict1['token']) == {
        'channels': [{3054207, 'PCSoc'}]
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

def test_channel_reinvite():
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

    # Test leaves PCSoc
    channel_leave(reg_dict1['token'], createDict2['token'])

    # Sabine reinvites Test to PCSoc
    assert channel_invite(reg_dict2['token'], create_dict2['channel_id'], \
        reg_dict1['u_id']) == {}
    assert channels_list(reg_dict1['token']) == {
        'channels': [
            {3054207, 'PCSoc'},
            {7654321, '1531 autotest'}
        ]
    }

    # Check that Sabine's channel list was unmodified
    assert channels_list(reg_dict2['token']) == {
        'channels': [{3054207, 'PCSoc'}]
    }

#########################
# channel_details Tests #
#########################

def test_channel_details_simple():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    create_dict2 = channels_create(reg_dict2['token'], 'PCSoc', False)
    create_dict3 = channels_create(reg_dict3['token'], 'Steam', True)

    channel_invite(reg_dict2['token'], create_dict2['channel_id'], \
        reg_dict1['u_id']) == {}

    channel_join(reg_dict1['token'], create_dict3['channel_id'])
    # SETUP END

    # Check 1531 autotest channel details
    detail1 = channel_details(reg_dict1['token'], create_dict1['channel_id'])
    assert detail1 and 'name' in detail1 and 'owner_members' in detail1 \
        and 'all_members' in detail1
    assert detail1['name'] == '1531 autotest'
    assert detail1['owner_members'] == [{
        'u_id': reg_dict1['u_id'],
        'name_first': 'Test',
        'name_last': 'User'
    }]
    assert detail1['all_members'] == [{
        'u_id': reg_dict1['u_id'],
        'name_first': 'Test',
        'name_last': 'User'
    }]

    # Check PCSoc channel details
    detail2 = channel_details(reg_dict1['token'], create_dict2['channel_id'])
    assert detail2 and 'name' in detail2 and 'owner_members' in detail2 \
        and 'all_members' in detail2
    assert detail2['name'] == 'PCSoc'
    assert detail2['owner_members'] == [{
        'u_id': reg_dict2['u_id'],
        'name_first': 'Sabine',
        'name_last': 'Lim'
    }]
    assert {
        'u_id': reg_dict1['u_id'],
        'name_first': 'Test',
        'name_last': 'User'
    } in detail2['all_members']
    assert {
        'u_id': reg_dict2['u_id'],
        'name_first': 'Sabine',
        'name_last': 'Lim'
    } in detail2['all_members']
    assert {
        'u_id': reg_dict3['u_id'],
        'name_first': 'Gabe',
        'name_last': 'Newell'
    } not in detail2['all_members']

    # Check Steam channel details
    detail3 = channel_details(reg_dict1['token'], create_dict3['channel_id'])
    assert detail3 and 'name' in detail3 and 'owner_members' in detail3 \
        and 'all_members' in detail3
    assert detail3['name'] == 'PCSoc'
    assert detail3['owner_members'] == [{
        'u_id': reg_dict3['u_id'],
        'name_first': 'Gabe',
        'name_last': 'Newell'
    }]
    assert {
        'u_id': reg_dict1['u_id'],
        'name_first': 'Test',
        'name_last': 'User'
    } in detail2['all_members']
    assert {
        'u_id': reg_dict2['u_id'],
        'name_first': 'Sabine',
        'name_last': 'Lim'
    } not in detail2['all_members']
    assert {
        'u_id': reg_dict3['u_id'],
        'name_first': 'Gabe',
        'name_last': 'Newell'
    } in detail2['all_members']

def test_channel_details_notinchannel():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')

    create_dict1 = channels_create(reg_dict2['token'], 'PCSoc', False)
    create_dict2 = channels_create(reg_dict3['token'], 'Steam', True)
    # SETUP END

    with pytest.raises(AccessError):
        channel_details(reg_dict1['token'], create_dict1['channel_id'])

    with pytest.raises(AccessError):
        channel_details(reg_dict1['token'], create_dict2['channel_id'])

def test_channel_details_bad_channelid():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END

    with pytest.raises(ValueError):
        channel_details(reg_dict1['token'], create_dict1['channel_id'] + 1)

##########################
# channel_messages Tests #
##########################

def test_channel_messages_nomessages():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END

    assert channel_messages(reg_dict1['token'], ) == {
        'messages': [],
        'start': 0,
        'end': -1
    }

def test_channel_messages_exactly1():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)

    message_dict1 = message_send(reg_dict1['token'], create_dict1['channel_id'], 'Whats up')
    # SETUP END

    messages1 = channel_messages(reg_dict1['token'], create_dict1['channel_id'], 0)
    assert messages1
    assert 'messages' in messages1 and 'start' in messages1 and 'end' in messages1
    assert messages1['start'] == 0 and messages1['end'] == -1
    assert messages1['messages'][0]['u_id'] == reg_dict1['u_id']
    assert messages1['messages'][0]['message'] == 'Whats up'

def test_channel_messages_lesserthan50():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)

    channel_join(reg_dict2['token'], create_dict1['channel_id'])

    for x in range(15):
        message_send(reg_dict1['token'], create_dict1['channel_id'], 'Hey there')
        message_send(reg_dict2['token'], create_dict1['channel_id'], 'Whats up')
    # SETUP END

    messages1 = channel_messages(reg_dict1['token'], create_dict1['channel_id'], 0)
    assert messages1
    assert 'messages' in messages1 and 'start' in messages1 and 'end' in messages1
    assert messages1['start'] == 0 and messages1['end'] == -1

def test_channel_messages_exactly50():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)

    channel_join(reg_dict2['token'], create_dict1['channel_id'])

    for x in range(25):
        message_send(reg_dict1['token'], create_dict1['channel_id'], 'Hey there')
        message_send(reg_dict2['token'], create_dict1['channel_id'], 'Whats up')
    # SETUP END

    messages1 = channel_messages(reg_dict1['token'], create_dict1['channel_id'], 0)
    assert messages1
    assert 'messages' in messages1 and 'start' in messages1 and 'end' in messages1
    assert messages1['start'] == 0 and messages1['end'] == -1

def test_channel_messages_paginated():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)

    channel_join(reg_dict2['token'], create_dict1['channel_id'])

    for x in range(35):
        message_send(reg_dict1['token'], create_dict1['channel_id'], 'Hey there')
        message_send(reg_dict2['token'], create_dict1['channel_id'], 'Whats up')
    # SETUP END

    messages1 = channel_messages(reg_dict1['token'], create_dict1['channel_id'], 0)
    assert messages1
    assert 'messages' in messages1 and 'start' in messages1 and 'end' in messages1
    assert messages1['start'] == 0 and messages1['end'] == 49

    messages2 = channel_messages(reg_dict1['token'], create_dict1['channel_id'], 50)
    assert messages1
    assert 'messages' in messages1 and 'start' in messages1 and 'end' in messages1
    assert messages1['start'] == 50 and messages1['end'] == -1

def test_channel_messages_notinchannel():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)

    channel_join(reg_dict2['token'], create_dict1['channel_id'])
    # SETUP END

    # Sabine attempts to read messages from the empty 1531 autotest channel
    with pytest.raises(AccessError):
        channel_messages(reg_dict2['token'], create_dict1['channel_id'], 0)

    # Test sends some messages in 1531 autotest
    for x in range(70):
        message_send(reg_dict1['token'], create_dict1['channel_id'], 'Hey there')

    # Sabine attempts to read messages from 1531 autotest
    with pytest.raises(AccessError):
        channel_messages(reg_dict2['token'], create_dict1['channel_id'], 0)

def test_channel_messages_bad_channelid():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)

    for x in range(70):
        message_send(reg_dict1['token'], create_dict1['channel_id'], 'Hey there')
    # SETUP END

    with pytest.raises(ValueError):
        channel_messages(reg_dict1['token'], create_dict1['channel_id'] + 1, 0)

def test_channel_messages_bad_startno():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)

    channel_join(reg_dict2['token'], create_dict1['channel_id'])
    # SETUP END

    with pytest.raises(ValueError):
        channel_messages(reg_dict1['token'], create_dict1['channel_id'], 0)

    for x in range(35):
        message_send(reg_dict1['token'], create_dict1['channel_id'], 'Hey there')
        message_send(reg_dict2['token'], create_dict1['channel_id'], 'Whats up')

    with pytest.raises(ValueError):
        channel_messages(reg_dict1['token'], create_dict1['channel_id'], 100)

#######################
# channel_leave Tests #
#######################

def test_channel_leave_simple():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    create_dict2 = channels_create(reg_dict2['token'], 'PCSoc', False)
    create_dict3 = channels_create(reg_dict3['token'], 'Steam', True)

    channel_join(reg_dict2['token'], create_dict1['channel_id'])
    channel_join(reg_dict3['token'], create_dict1['channel_id'])
    # SETUP END

    # Sabine leaves 1531 autotest
    assert channel_leave(reg_dict2['token'], create_dict1['channel_id']) == {}
    assert channels_list(reg_dict2['token']) == {
        'channels': [{3054207, 'PCSoc'}]
    }

    # Gabe leaves 1531 autotest
    assert channel_leave(reg_dict3['token'], create_dict1['channel_id']) == {}
    assert channels_list(reg_dict3['token']) == {
        'channels': [{9703358, 'Steam'}]
    }

def test_channel_leave_lastuser():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END

    assert channel_leave(reg_dict1['token'], create_dict1['channel_id']) == {}
    assert channels_list(reg_dict1['token']) == {'channels': []}

# Will implement this test after interface is clarified (see assumptions.md)
def test_channel_leave_owner():
    pass

def test_channel_leave_lastchannel():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)

    channel_join(reg_dict2['token'], create_dict1['channel_id'])
    # SETUP END

    assert channel_leave(reg_dict2['token'], create_dict1['channel_id']) == {}
    assert channels_list(reg_dict2['token']) == {'channels': []}

def test_channel_leave_private():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict2['token'], 'PCSoc', False)

    channel_join(reg_dict1['token'], create_dict1['channel_id'])
    # SETUP END

    assert channel_leave(reg_dict1['token'], create_dict1['channel_id']) == {}
    assert channels_list(reg_dict1['token']) == {'channels': []}

def test_channel_leave_notinchannel():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END

    with pytest.raises(ValueError):
        channel_leave(reg_dict2['token'], create_dict1['channel_id'])

def test_channel_leave_bad_channelid():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END

    with pytest.raises(ValueError):
        channel_leave(reg_dict1['token'], create_dict1['channel_id'] + 1)

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
    assert channel_join(reg_dict2['token'], create_dict3['channel_id']) == {}

    # Gabe joins 1531 autotest
    assert channel_join(reg_dict3['token'], create_dict1['channel_id']) == {}

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

def test_channel_join_no_autoowner():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict2['token'], 'PCSoc', False)
    # SETUP END

    # Test joins PCSoc, check that Test not automatically owner of PCSoc
    assert channel_join(reg_dict1['token'], create_dict1['channel_id']) == {}
    assert {
        'u_id': reg_dict1['u_id'],
        'name_first': 'Test',
        'name_last': 'User'
    } not in channel_details(reg_dict1['token'], create_dict1['channel_id'])['owner_members']

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

def test_channel_join_private():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict2['token'], 'PCSoc', False)
    # SETUP END

    # Test attempts to join PCSoc
    assert channel_join(reg_dict1['token'], create_dict1['channel_id']) == {}
    assert channels_list(reg_dict1['token']) == {
        'channels': [{3054207, 'PCSoc'}]
    }

    # Check that Sabine's channel list was unmodified
    assert channels_list(reg_dict2['token']) == {
        'channels': [{3054207, 'PCSoc'}]
    }

def test_channel_rejoin():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict2['token'], 'PCSoc', True)
    # SETUP END

    # Test joins PCSoc
    assert channel_join(reg_dict1['token'], create_dict1['channel_id']) == {}
    assert channels_list(reg_dict1['token']) == {
        'channels': [{7654321, '1531 autotest'}]
    }

    # Test leaves PCSoc
    channel_leave(reg_dict1['token'], create_dict1['channel_id'])

    # Test rejoins PCSoc
    assert channel_join(reg_dict1['token'], create_dict1['channel_id']) == {}
    assert channels_list(reg_dict1['token']) == {
        'channels': [{7654321, '1531 autotest'}]
    }

    # Check that Sabine's channel list was unmodified
    assert channels_list(reg_dict2['token']) == {
        'channels': [{3054207, 'PCSoc'}]
    }

def test_channel_rejoin_private():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict2['token'], 'PCSoc', False)
    # SETUP END

    # Test joins PCSoc
    assert channel_join(reg_dict1['token'], create_dict1['channel_id']) == {}
    assert channels_list(reg_dict1['token']) == {
        'channels': [{7654321, '1531 autotest'}]
    }

    # Test leaves PCSoc
    channel_leave(reg_dict1['token'], create_dict1['channel_id'])

    # Test rejoins PCSoc
    assert channel_join(reg_dict1['token'], create_dict1['channel_id']) == {}
    assert channels_list(reg_dict1['token']) == {
        'channels': [{7654321, '1531 autotest'}]
    }

    # Check that Sabine's channel list was unmodified
    assert channels_list(reg_dict2['token']) == {
        'channels': [{3054207, 'PCSoc'}]
    }

##########################
# channel_addowner Tests #
##########################

def test_channel_addowner_simple():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    create_dict2 = channels_create(reg_dict2['token'], 'PCSoc', False)
    create_dict3 = channels_create(reg_dict3['token'], 'Steam', True)

    channel_invite(reg_dict2['token'], create_dict2['channel_id'], reg_dict1['u_id'])

    channel_join(reg_dict2['token'], create_dict1['channel_id'])
    channel_join(reg_dict2['token'], create_dict3['channel_id'])
    # SETUP END

    # Sabine adds Test as owner of PCSoc
    assert channel_addowner(reg_dict2['token'], create_dict2['channel_id'], \
        reg_dict1['u_id']) == {}
    assert {
        'u_id': reg_dict1['u_id'],
        'name_first': 'Test',
        'name_last': 'User'
    } in channel_details(reg_dict1['token'], create_dict2['channel_id'])['owner_members']

    # Test adds Sabine as owner of 1531 autotest
    assert channel_addowner(reg_dict1['token'], create_dict1['channel_id'], \
        reg_dict2['u_id']) == {}
    assert {
        'u_id': reg_dict2['u_id'],
        'name_first': 'Sabine',
        'name_last': 'Lim'
    } in channel_details(reg_dict1['token'], create_dict2['channel_id'])['owner_members']

    # Gabe adds Sabine as owner of 1531 autotest
    assert channel_addowner(reg_dict3['token'], create_dict3['channel_id'], \
        reg_dict2['u_id']) == {}
    assert {
        'u_id': reg_dict2['u_id'],
        'name_first': 'Sabine',
        'name_last': 'Lim'
    } in channel_details(reg_dict1['token'], create_dict2['channel_id'])['owner_members']

def test_channel_addowner_slackrowner_promoteself():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict2['token'], 'PCSoc', False)

    channel_join(reg_dict1['token'], create_dict1['channel_id'])
    # SETUP END

    # Test adds self as owner of PCSoc
    assert channel_addowner(reg_dict1['token'], create_dict1['channel_id'], \
        reg_dict1['u_id']) == {}
    assert {
        'u_id': reg_dict1['u_id'],
        'name_first': 'Test',
        'name_last': 'User'
    } in channel_details(reg_dict1['token'], create_dict1['channel_id'])['owner_members']

def test_channel_addowner_slackrowner_promoteother_notchannelowner():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')

    create_dict1 = channels_create(reg_dict2['token'], 'PCSoc', False)

    channel_join(reg_dict1['token'], create_dict1['channel_id'])

    channel_invite(reg_dict1['token'], create_dict1['channel_id'], reg_dict3['u_id'])
    # SETUP END

    # Test adds Gabe as owner of PCSoc
    assert channel_addowner(reg_dict1['token'], create_dict1['channel_id'], \
        reg_dict3['u_id']) == {}
    assert {
        'u_id': reg_dict3['u_id'],
        'name_first': 'Gabe',
        'name_last': 'Newell'
    } in channel_details(reg_dict1['token'], create_dict1['channel_id'])['owner_members']

# Will need to write this test after interface is clarified
def test_channel_addowner_target_notinchannel():
    pass

def test_channel_addowner_user_notinchannel():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    create_dict2 = channels_create(reg_dict2['token'], 'PCSoc', False)

    channel_join(reg_dict3['token'], create_dict2['channel_id'])

    channel_join(reg_dict3['token'], create_dict1['channel_id'])

    channel_join(reg_dict1['token'], create_dict2['channel_id'])
    # SETUP END

    # Test attempts to add Gabe as owner of PCSoc
    with pytest.raises(AccessError):
        channel_addowner(reg_dict1['token'], create_dict2['channel_id'], reg_dict3['u_id'])

    # Sabine attempts to add Gabe as owner of 1531 autotest
    with pytest.raises(AccessError):
        channel_addowner(reg_dict2['token'], create_dict1['channel_id'], reg_dict3['u_id'])

    # Gabe attempts to add Test as owner of PCSoc
    with pytest.raises(AccessError):
        channel_addowner(reg_dict3['token'], create_dict2['channel_id'], reg_dict1['u_id'])

def test_channel_addowner_bad_channelid():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)

    channel_join(reg_dict2['token'], create_dict1['channel_id'])
    # SETUP END

    with pytest.raises(ValueError):
        channel_addowner(reg_dict1['token'], create_dict1['channel_id'] + 1, reg_dict2['u_id'])

def test_channel_addowner_target_alreadyowner():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)

    channel_join(reg_dict2['token'], create_dict1['channel_id'])
    # SETUP END

    assert channel_addowner(reg_dict1['token'], create_dict1['channel_id'], \
        reg_dict2['u_id']) == {}

    with pytest.raises(ValueError):
        channel_addowner(reg_dict1['token'], create_dict1['channel_id'], reg_dict2['u_id'])

def test_channel_addowner_noperms():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)

    channel_join(reg_dict3['token'], create_dict1['channel_id'])
    # SETUP END

    # Sabine attempts to add Gabe as owner of 1531 autotest
    with pytest.raises(AccessError):
        channel_addowner(reg_dict2['token'], create_dict1['channel_id'], reg_dict3['u_id'])

    # Sabine joins 1531 autotest
    channel_join(reg_dict2['token'], create_dict1['channel_id'])

    # Sabine attempts to add Gabe as owner of 1531 autotest
    with pytest.raises(ValueError):
        channel_addowner(reg_dict2['token'], create_dict1['channel_id'], reg_dict3['u_id'])

#############################
# channel_removeowner Tests #
#############################

def test_channel_removeowner_simple():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    create_dict2 = channels_create(reg_dict2['token'], 'PCSoc', False)
    create_dict3 = channels_create(reg_dict3['token'], 'Steam', True)

    channel_invite(reg_dict2['token'], create_dict2['channel_id'], reg_dict1['u_id'])

    channel_join(reg_dict2['token'], create_dict1['channel_id'])
    channel_join(reg_dict2['token'], create_dict3['channel_id'])

    channel_addowner(reg_dict2['token'], create_dict2['channel_id'], reg_dict1['u_id'])

    channel_addowner(reg_dict1['token'], create_dict1['channel_id'], reg_dict2['u_id'])

    channel_addowner(reg_dict3['token'], create_dict3['channel_id'], reg_dict2['u_id'])
    # SETUP END

    # Sabine removes Test as owner of PCSoc
    assert channel_removeowner(reg_dict2['token'], create_dict2['channel_id'], \
        reg_dict1['u_id']) == {}
    assert {
        'u_id': reg_dict1['u_id'],
        'name_first': 'Test',
        'name_last': 'User'
    } not in channel_details(reg_dict1['token'], create_dict2['channel_id'])['owner_members']

    # Test removes Sabine as owner of 1531 autotest
    assert channel_removeowner(reg_dict1['token'], create_dict1['channel_id'], \
        reg_dict2['u_id']) == {}
    assert {
        'u_id': reg_dict2['u_id'],
        'name_first': 'Sabine',
        'name_last': 'Lim'
    } not in channel_details(reg_dict1['token'], create_dict2['channel_id'])['owner_members']

    # Gabe removes Sabine as owner of 1531 autotest
    assert channel_removeowner(reg_dict3['token'], create_dict3['channel_id'], \
        reg_dict2['u_id']) == {}
    assert {
        'u_id': reg_dict2['u_id'],
        'name_first': 'Sabine',
        'name_last': 'Lim'
    } not in channel_details(reg_dict1['token'], create_dict2['channel_id'])['owner_members']

def test_channel_removeowner_slackrowner_demoteother_notchannelowner():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')

    create_dict1 = channels_create(reg_dict2['token'], 'PCSoc', False)

    channel_join(reg_dict1['token'], create_dict1['channel_id'])

    channel_invite(reg_dict1['token'], create_dict1['channel_id'], reg_dict3['u_id'])

    channel_addowner(reg_dict2['token'], create_dict1['channel_id'], reg_dict3['u_id'])
    # SETUP END

    # Test removes Gabe as owner of PCSoc
    assert channel_removeowner(reg_dict1['token'], create_dict1['channel_id'], \
        reg_dict3['u_id']) == {}
    assert {
        'u_id': reg_dict3['u_id'],
        'name_first': 'Gabe',
        'name_last': 'Newell'
    } not in channel_details(reg_dict1['token'], create_dict1['channel_id'])['owner_members']

# Will need to write this test after interface is clarified
def test_channel_removeowner_target_notinchannel():
    pass

def test_channel_removeowner_user_notinchannel():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    create_dict2 = channels_create(reg_dict2['token'], 'PCSoc', False)

    channel_join(reg_dict3['token'], create_dict2['channel_id'])
    channel_addowner(reg_dict2['token'], create_dict2['channel_id'], reg_dict3['u_id'])

    channel_join(reg_dict3['token'], create_dict1['channel_id'])
    channel_addowner(reg_dict1['token'], create_dict1['channel_id'], reg_dict3['u_id'])

    channel_join(reg_dict1['token'], create_dict2['channel_id'])
    channel_addowner(reg_dict2['token'], create_dict2['channel_id'], reg_dict1['u_id'])
    # SETUP END

    # Test attempts to remove Gabe as owner of PCSoc
    with pytest.raises(AccessError):
        channel_removeowner(reg_dict1['token'], create_dict2['channel_id'], reg_dict3['u_id'])

    # Sabine attempts to remove Gabe as owner of 1531 autotest
    with pytest.raises(AccessError):
        channel_removeowner(reg_dict2['token'], create_dict1['channel_id'], reg_dict3['u_id'])

    # Gabe attempts to remove Test as owner of PCSoc
    with pytest.raises(AccessError):
        channel_removeowner(reg_dict3['token'], create_dict2['channel_id'], reg_dict1['u_id'])

def test_channel_removeowner_bad_channelid():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)

    channel_join(reg_dict2['token'], create_dict1['channel_id'])
    channel_addowner(reg_dict1['token'], create_dict1['channel_id'], reg_dict2['u_id'])
    # SETUP END

    with pytest.raises(ValueError):
        channel_removeowner(reg_dict1['token'], create_dict1['channel_id'] + 1, reg_dict2['u_id'])

def test_channel_removeowner_target_notowner():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)

    channel_join(reg_dict2['token'], create_dict1['channel_id'])
    # SETUP END

    with pytest.raises(ValueError):
        channel_removeowner(reg_dict1['token'], create_dict1['channel_id'], reg_dict2['u_id'])

def test_channel_removeowner_noperms():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)

    channel_join(reg_dict3['token'], create_dict1['channel_id'])

    channel_addowner(reg_dict1['u_id'], create_dict1['channel_id'], reg_dict3['u_id'])
    # SETUP END

    # Sabine attempts to remove Gabe as owner of 1531 autotest
    with pytest.raises(AccessError):
        channel_addowner(reg_dict2['token'], create_dict1['channel_id'], reg_dict3['u_id'])

    # Sabine joins 1531 autotest
    channel_join(reg_dict2['token'], create_dict1['channel_id'])

    # Sabine attempts to remove Gabe as owner of 1531 autotest
    with pytest.raises(ValueError):
        channel_removeowner(reg_dict2['token'], create_dict1['channel_id'], reg_dict3['u_id'])
