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
