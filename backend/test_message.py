# COMP1531 Project test_message
# Written by Bridget McCarthy z5255505 and Sabine Lim z5242579
# 29/09/19

import pytest
import time

from .db import reset_data, db_add_time_offset, db_reset_time_offset
from .auth import auth_register
from .message import (
    message_send, message_sendlater, message_edit, message_remove, message_pin,
    message_unpin, message_react, message_unreact
)
from .channel import (
    channel_join, channel_invite, channel_leave, channel_addowner,
    channel_messages
)
from .channels import channels_create
from .error import ValueError, AccessError

###########################
# message_sendlater Tests #
###########################

def test_message_sendlater_simple():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], create_dict1['channel_id'])
    channel_join(reg_dict3['token'], create_dict1['channel_id'])
    # SETUP END

    now = time.time()

    # Send a message in 10 minutes
    now_plus_mins = now + 10 * 60
    message_dict1 = message_sendlater(reg_dict1['token'], create_dict1['channel_id'], "Oof", now_plus_mins)
    
    # Send a message in 1 hour
    now_plus_hour = now + 60 * 60
    message_dict2 = message_sendlater(reg_dict2['token'], create_dict1['channel_id'], "Ouch", now_plus_hour)

    # Send a message in 3 days
    now_plus_days = now + 3 * 24 * 60 * 60
    message_dict3 = message_sendlater(reg_dict3['token'], create_dict1['channel_id'], "Owie", now_plus_days)

    # Check message send attempts returned different ids
    assert message_dict1['message_id'] != message_dict2['message_id'] != message_dict3['message_id']

    # Check messages at present time
    assert channel_messages(reg_dict1['token'], create_dict1['channel_id'], 0)['messages'] == []

    # Manipulate time to 10 minutes in the future and check messages
    db_add_time_offset(10 * 60)
    assert channel_messages(reg_dict1['token'], create_dict1['channel_id'], 0)['messages'] == [
        {
            'message_id': message_dict1['message_id'],
            'u_id': create_dict1['u_id'],
            'message': 'Oof',
            'time_created': now_plus_mins,
            'reacts': [],
            'is_pinned': False
        }
    ]

    # Manipulate time to 1 hour in the future and check messages
    db_reset_time_offset()
    db_add_time_offset(60 * 60)
    assert channel_messages(reg_dict2['token'], create_dict1['channel_id'], 0)['messages'] == [
        {
            'message_id': message_dict2['message_id'],
            'u_id': create_dict1['u_id'],
            'message': 'Ouch',
            'time_created': now_plus_hour,
            'reacts': [],
            'is_pinned': False
        },
        {
            'message_id': message_dict1['message_id'],
            'u_id': create_dict1['u_id'],
            'message': 'Oof',
            'time_created': now_plus_mins,
            'reacts': [],
            'is_pinned': False
        }
    ]

    # Manipulate time to 3 days in the future and check messages
    db_reset_time_offset()
    db_add_time_offset(3 * 24 * 60 * 60)
    assert channel_messages(reg_dict2['token'], create_dict1['channel_id'], 0)['messages'] == [
        {
            'message_id': message_dict3['message_id'],
            'u_id': create_dict1['u_id'],
            'message': 'Ouch',
            'time_created': now_plus_days,
            'reacts': [],
            'is_pinned': False
        },
        {
            'message_id': message_dict2['message_id'],
            'u_id': create_dict1['u_id'],
            'message': 'Ouch',
            'time_created': now_plus_hour,
            'reacts': [],
            'is_pinned': False
        },
        {
            'message_id': message_dict1['message_id'],
            'u_id': create_dict1['u_id'],
            'message': 'Oof',
            'time_created': now_plus_mins,
            'reacts': [],
            'is_pinned': False
        }
    ]

def test_message_sendlater_long_message():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    create_dict2 = channels_create(reg_dict2['token'], 'PCSoc', False)
    # SETUP END

    now = time.time()

    # Attempt to send a too long message in 10 minutes
    now_plus_mins = now + 10 * 60
    too_long_msg = "If you take the temperature of a superconductor down to absolute zero (around minus 273.1 centigrade), it ignores gravity and floats. This is a scientific fact and you are welcome to check - google or youtube it. My 9yo son asked why we couldn't freeze a car to -273C and fly in it and I told him that the car would neutralise gravity, not reverse it and the weight of the people in it would make it sink. Also, heat rises so -273C should really sink unless it was in a vacuum which means we wouldn't be able to breath or hear the stereo. You would also need to rug up well. If you take the temperature of a superconductor down to absolute zero (around minus 273.1 centigrade), it ignores gravity and floats. This is a scientific fact and you are welcome to check - google or youtube it. My 9yo son asked why we couldn't freeze a car to -273C and fly in it and I told him that the car would neutralise gravity, not reverse it and the weight of the people in it would make it sink. Also, heat rises so -273C should really sink unless it was in a vacuum which means we wouldn't be able to breath or hear the stereo. You would also need to rug up well."
    with pytest.raises(ValueError):
        message_sendlater(reg_dict1['token'], create_dict1['channel_id'], too_long_msg, now_plus_mins)
    with pytest.raises(ValueError):
        message_sendlater(reg_dict2['token'], create_dict2['channel_id'], too_long_msg, now_plus_mins)
    
def test_message_sendlater_empty_message():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    create_dict2 = channels_create(reg_dict1['token'], 'PCSoc', False)
    # SETUP END

    now = time.time()

    # Test attempts to send an empty message 10 minutes in the future
    now_plus_minutes = now + 10 * 60
    with pytest.raises(ValueError):
        message_sendlater(reg_dict1['token'], create_dict1['channel_id'], "", now_plus_minutes)

    # Sabine attempts to send an empty message 10 hours in the future
    now_plus_hours = now + 10 * 60 * 60
    with pytest.raises(ValueError):
        message_sendlater(reg_dict2['token'], create_dict2['channel_id'], "", now_plus_hours)
    
def test_message_sendlater_invalid_channel():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END

    now = time.time()

    # Attempt to send messages to invalid channel ids in 10 minutes
    now_plus_mins = now + 10 * 60
    channel_id = create_dict1['channel_id'] + 1
    with pytest.raises(ValueError):
        message_sendlater(reg_dict1['token'], channel_id, "Oof", now_plus_mins)
    channel_id += 1
    with pytest.raises(ValueError):
        message_sendlater(reg_dict1['token'], channel_id, "Oof", now_plus_mins)
    channel_id += 1
    with pytest.raises(ValueError):
        message_sendlater(reg_dict1['token'], channel_id, "Oof", now_plus_mins)

def test_message_sendlater_past_time():
     # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')  

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)

    now = time.time()
    # SETUP END

    # Attempt to send a message 10 seconds in the past
    now_minus_seconds = now - 10
    with pytest.raises(ValueError):
        message_sendlater(reg_dict1['token'], create_dict1['channel_id'], "Oof", now_minus_seconds)

    # Attempt to send a message 10 minutes in the past
    now_minus_mins = now - 10 * 60
    with pytest.raises(ValueError):
        message_sendlater(reg_dict1['token'], create_dict1['channel_id'], "Oof", now_minus_mins)

    # Attempt to send a message 10 hours in the past
    now_minus_hours = now - 10 * 60 * 60
    with pytest.raises(ValueError):
        message_sendlater(reg_dict1['token'], create_dict1['channel_id'], "Oof", now_minus_hours)

    # Attempt to send a message 10 days in the past
    now_minus_days = now - 10 * 24 * 60 * 60
    with pytest.raises(ValueError):
        message_sendlater(reg_dict1['token'], create_dict1['channel_id'], "Oof", now_minus_days)

def test_message_sendlater_not_in_channel():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    create_dict2 = channels_create(reg_dict2['token'], 'PCSoc', False)
    # SETUP END

    now = time.time()

    # Test attempts to send a message to PCSoc in 10 minutes
    now_plus_mins = now + 10 * 60
    with pytest.raises(AccessError):
        message_sendlater(reg_dict1['token'], create_dict2['channel_id'], "Oof", now_plus_mins)
    
    # Sabine attempt to send a message to 1531 autotest in 1 hour
    now_plus_hour = now + 60 * 60
    with pytest.raises(AccessError):
        message_sendlater(reg_dict2['token'], create_dict1['channel_id'], "Ouch", now_plus_hour)

    # Gabe attempts to send a message to 1531 autotest in 3 days
    now_plus_days = now + 3 * 24 * 60 * 60
    with pytest.raises(AccessError):
        message_sendlater(reg_dict3['token'], create_dict1['channel_id'], "Owie", now_plus_days)
    
######################
# message_send Tests #
######################

def test_message_send_simple():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], create_dict1['channel_id'])
    channel_join(reg_dict3['token'], create_dict1['channel_id'])
    # SETUP END

    # Test sends a message
    message_dict1 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Oof")
    channel_message1 = channel_messages(reg_dict1['token'], create_dict1['channel_id'], 0)['messages'][0]
    assert channel_message1['message_id'] == message_dict1['message_id']
    assert channel_message1['u_id'] == reg_dict1['u_id']
    assert channel_message1['message'] == 'Oof'

    message_dict2 = message_send(reg_dict2['token'], create_dict1['channel_id'], "Ouch")
    channel_message2 = channel_messages(reg_dict2['token'], create_dict1['channel_id'], 0)['messages'][0]
    assert channel_message2['message_id'] == message_dict2['message_id']
    assert channel_message2['u_id'] == reg_dict2['u_id']
    assert channel_message2['message'] == 'Ouch'

    message_dict3 = message_send(reg_dict3['token'], create_dict1['channel_id'], "Owie")
    channel_message3 = channel_messages(reg_dict3['token'], create_dict1['channel_id'], 0)['messages'][0]
    assert channel_message3['message_id'] == message_dict3['message_id']
    assert channel_message3['u_id'] == reg_dict3['u_id']
    assert channel_message3['message'] == 'Ouch'
    
    # Check message send attempts returned different ids
    assert message_dict1['message_id'] != message_dict2['message_id'] != message_dict3['message_id']

def test_message_send_too_long_message():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    create_dict2 = channels_create(reg_dict2['token'], 'PCSoc', False)
    # SETUP END

    too_long_msg = "If you take the temperature of a superconductor down to absolute zero (around minus 273.1 centigrade), it ignores gravity and floats. This is a scientific fact and you are welcome to check - google or youtube it. My 9yo son asked why we couldn't freeze a car to -273C and fly in it and I told him that the car would neutralise gravity, not reverse it and the weight of the people in it would make it sink. Also, heat rises so -273C should really sink unless it was in a vacuum which means we wouldn't be able to breath or hear the stereo. You would also need to rug up well. If you take the temperature of a superconductor down to absolute zero (around minus 273.1 centigrade), it ignores gravity and floats. This is a scientific fact and you are welcome to check - google or youtube it. My 9yo son asked why we couldn't freeze a car to -273C and fly in it and I told him that the car would neutralise gravity, not reverse it and the weight of the people in it would make it sink. Also, heat rises so -273C should really sink unless it was in a vacuum which means we wouldn't be able to breath or hear the stereo. You would also need to rug up well."
    with pytest.raises(ValueError):
        message_send(reg_dict1['token'], create_dict1['channel_id'], too_long_msg)
    with pytest.raises(ValueError):
        message_send(reg_dict2['token'], create_dict2['channel_id'], too_long_msg)
    
def test_message_send_empty_message():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    create_dict2 = channels_create(reg_dict1['token'], 'PCSoc', False)
    # SETUP END

    with pytest.raises(ValueError):
        message_send(reg_dict1['token'], create_dict1['channel_id'], "")
    with pytest.raises(ValueError):
        message_send(reg_dict2['token'], create_dict2['channel_id'], "")
    
def test_message_send_invalid_channel():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END

    # Attempt to send messages to invalid channel ids
    channel_id = create_dict1['channel_id'] + 1
    with pytest.raises(ValueError):
        message_send(reg_dict1['token'], channel_id, "Oof")
    channel_id += 1
    with pytest.raises(ValueError):
        message_send(reg_dict1['token'], channel_id, "Oof")
    channel_id += 1
    with pytest.raises(ValueError):
        message_send(reg_dict1['token'], channel_id, "Oof")

def test_message_send_not_in_channel():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    create_dict2 = channels_create(reg_dict2['token'], 'PCSoc', False)
    # SETUP END

    # Test attempts to send a message to PCSoc
    with pytest.raises(AccessError):
        message_send(reg_dict1['token'], create_dict2['channel_id'], "Oof")
    
    # Sabine attempt to send a message to 1531 autotest
    with pytest.raises(AccessError):
        message_send(reg_dict2['token'], create_dict1['channel_id'], "Ouch")

    # Gabe attempts to send a message to 1531 autotest
    with pytest.raises(AccessError):
        message_send(reg_dict3['token'], create_dict1['channel_id'], "Owie")

########################
# message_remove Tests #
########################

def test_message_remove_simple():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    create_dict2 = channels_create(reg_dict2['token'], 'PCSoc', False)

    message_dict1 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Oof")
    message_dict2 = message_send(reg_dict2['token'], create_dict2['channel_id'], "Ouch")
    # SETUP END

    assert message_remove(reg_dict1['token'], message_dict1['message_id']) == {}
    assert message_remove(reg_dict2['token'], message_dict2['message_id']) == {}

def test_message_remove_already_removed():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    create_dict2 = channels_create(reg_dict2['token'], 'PCSoc', False)

    message_dict1 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Oof")
    message_dict2 = message_send(reg_dict2['token'], create_dict2['channel_id'], "Ouch")
    # SETUP END

    assert message_remove(reg_dict1['token'], message_dict1['message_id']) == {}
    assert message_remove(reg_dict2['token'], message_dict2['message_id']) == {}

    with pytest.raises(ValueError):
        message_remove(reg_dict1['token'], message_dict1['message_id'])
    with pytest.raises(ValueError):
        message_remove(reg_dict2['token'], message_dict2['message_id'])

def test_message_remove_invalid_message_id():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)

    message_dict1 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Oof")
    # SETUP END

    with pytest.raises(ValueError):
        message_remove(reg_dict1['token'], message_dict1['message_id'] + 1)

def test_message_remove_not_in_channel():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], create_dict1['channel_id'])

    create_dict2 = channels_create(reg_dict2['token'], 'PCSoc', False)
    channel_invite(reg_dict2['token'], create_dict2['channel_id'], reg_dict1['u_id'])

    message_dict1 = message_send(reg_dict1['token'], create_dict2['channel_id'], "Oof")
    message_dict2 = message_send(reg_dict2['token'], create_dict1['channel_id'], "Ouch")

    channel_leave(reg_dict1['token'], create_dict2['channel_id'])
    channel_leave(reg_dict2['token'], create_dict1['channel_id'])
    # SETUP END

    with pytest.raises(AccessError):
        message_remove(reg_dict2['token'], message_dict1['message_id'])
    with pytest.raises(AccessError):
        message_remove(reg_dict1['token'], message_dict2['message_id'])

def test_message_remove_message_not_sender():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], create_dict1['channel_id'])
    channel_join(reg_dict3['token'], create_dict1['channel_id'])

    create_dict2 = channels_create(reg_dict2['token'], 'PCSoc', False)
    channel_invite(reg_dict2['token'], create_dict2['channel_id'], reg_dict1['u_id'])
    channel_invite(reg_dict2['token'], create_dict2['channel_id'], reg_dict3['u_id'])

    message_dict1 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Message 1")
    message_dict2 = message_send(reg_dict2['token'], create_dict1['channel_id'], "Message 2")
    message_dict3 = message_send(reg_dict1['token'], create_dict2['channel_id'], "Message 3")
    message_dict4 = message_send(reg_dict2['token'], create_dict2['channel_id'], "Message 4")
    # SETUP END

    # Message can't be deleted by regular user who didn't send the message
    with pytest.raises(AccessError):
        message_remove(reg_dict3['token'], message_dict2['message_id'])

    # Message sent by owner of the channel, can't be deleted by regular users
    with pytest.raises(AccessError):
        message_remove(reg_dict2['token'], message_dict1['message_id'])
    with pytest.raises(AccessError):
        message_remove(reg_dict3['token'], message_dict1['message_id'])

    # Regular user gains ability to remove others' messages when they become
    # channel owner, including messages from other channel owners
    channel_addowner(reg_dict1['token'], create_dict1['channel_id'], reg_dict3['u_id'])
    assert message_remove(reg_dict3['token'], message_dict2['message_id']) == {}
    assert message_remove(reg_dict3['token'], message_dict1['message_id']) == {}

    # Owners of one channel can't delete others' messages from other channels
    # they aren't owner of
    with pytest.raises(AccessError):
        message_remove(reg_dict3['token'], message_dict3['message_id'])
    with pytest.raises(AccessError):
        message_remove(reg_dict3['token'], message_dict4['message_id'])

    # Unless they're a Slackr admin/owner
    assert message_remove(reg_dict1['token'], message_dict4) == {}

##############################
#     message_edit  Tests    #
##############################
# Probably subject to change as it seems the error conditions are completely
# wrong.
# i.e. Anybody can edit anybodies message
def test_message_edit_simple():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    channel_1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], channel_1['channel_id'])
    channel_join(reg_dict3['token'], channel_1['channel_id'])

    message_send(reg_dict1['token'], channel_1['channel_id'], "Message 0")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Oof")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Ouch")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Owie")

    channel_2 = channels_create(reg_dict1['token'], 'PCSoc', True)
    channel_join(reg_dict2['token'], channel_2['channel_id'])

    message_send(reg_dict2['token'], channel_2['channel_id'], "Oof")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Ouch")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Owie")
    # SETUP END

    # Users that made their own posts can edit them just fine
    # The text can still be the exact same as the original
    message_edit(reg_dict1['token'], 1, "Oof")
    message_edit(reg_dict1['token'], 2, "Ouch")
    message_edit(reg_dict1['token'], 3, "Owie")

    message_edit(reg_dict1['token'], 1, "OOF")
    message_edit(reg_dict1['token'], 2, "OUCH")
    message_edit(reg_dict1['token'], 3, "OWIE")

    message_edit(reg_dict2['token'], 4, "OOF")
    message_edit(reg_dict2['token'], 5, "OUCH")
    message_edit(reg_dict2['token'], 6, "OWIE")

    # Newly made messages can be immediately edited as well
    message_send(reg_dict3['token'], channel_2['channel_id'], "help")
    message_edit(reg_dict3['token'], 7, "Message 7")


def test_message_edit_wrong_user():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    channel_1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], channel_1['channel_id'])
    channel_join(reg_dict3['token'], channel_1['channel_id'])

    message_send(reg_dict1['token'], channel_1['channel_id'], "Message 0")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Oof")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Ouch")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Owie")

    channel_2 = channels_create(reg_dict1['token'], 'PCSoc', True)
    channel_join(reg_dict3['token'], channel_2['channel_id'])

    message_send(reg_dict2['token'], channel_2['channel_id'], "Oof")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Ouch")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Owie")
    # SETUP END
    # Regular User can edit messages they sent but not others
    message_send(reg_dict2['token'], channel_1['channel_id'], "User2")
    message_send(reg_dict3['token'], channel_1['channel_id'], "User3")
    with pytest.raises(ValueError):
        message_edit(reg_dict3['token'], 7, "i can't do this")
    with pytest.raises(ValueError):
        message_edit(reg_dict2['token'], 8, "i can't do this either")
    
    # Admins/owners of the channel can edit any other message in that channel
    message_edit(reg_dict1['token'], 7, "overridden")
    message_edit(reg_dict1['token'], 8, "deleted by admin")

    # A user made admin can edit messages for that channel
    channel_addowner(reg_dict1['token'], channel_1['channel_id'], reg_dict3['u_id'])
    message_edit(reg_dict3['token'], 7, "I CAN DO THIS NOW")
    # But still can't edit messages for channels they aren't an owner for
    with pytest.raises(ValueError):
        message_edit(reg_dict3['token'], 4, "i still can't do this")

def test_message_edit_invalid_message():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    channel_1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], channel_1['channel_id'])
    channel_join(reg_dict3['token'], channel_1['channel_id'])

    message_send(reg_dict1['token'], channel_1['channel_id'], "Message 0")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Oof")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Ouch")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Owie")

    channel_2 = channels_create(reg_dict1['token'], 'PCSoc', True)
    channel_join(reg_dict3['token'], channel_2['channel_id'])

    message_send(reg_dict2['token'], channel_2['channel_id'], "Oof")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Ouch")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Owie")
    # SETUP END

    # Messages must still abide by the 1000 char limit
    too_long_msg = "If you take the temperature of a superconductor down to absolute zero (around minus 273.1 centigrade), it ignores gravity and floats. This is a scientific fact and you are welcome to check - google or youtube it. My 9yo son asked why we couldn't freeze a car to -273C and fly in it and I told him that the car would neutralise gravity, not reverse it and the weight of the people in it would make it sink. Also, heat rises so -273C should really sink unless it was in a vacuum which means we wouldn't be able to breath or hear the stereo. You would also need to rug up well. If you take the temperature of a superconductor down to absolute zero (around minus 273.1 centigrade), it ignores gravity and floats. This is a scientific fact and you are welcome to check - google or youtube it. My 9yo son asked why we couldn't freeze a car to -273C and fly in it and I told him that the car would neutralise gravity, not reverse it and the weight of the people in it would make it sink. Also, heat rises so -273C should really sink unless it was in a vacuum which means we wouldn't be able to breath or hear the stereo. You would also need to rug up well."
    with pytest.raises(ValueError):
        message_edit(reg_dict1['token'], 0, too_long_msg)
    with pytest.raises(ValueError):
        message_edit(reg_dict2['token'], 4, too_long_msg)

    # Messages can't be empty
    with pytest.raises(ValueError):
        message_edit(reg_dict1['token'], 0, "")
    with pytest.raises(ValueError):
        message_edit(reg_dict1['token'], 1, "")
    with pytest.raises(ValueError):
        message_edit(reg_dict2['token'], 4, "")
    with pytest.raises(ValueError):
        message_edit(reg_dict2['token'], 5, "")

    # Message id must also be valid
    with pytest.raises(ValueError):
        message_edit(reg_dict1['token'], -1, "test")
    with pytest.raises(ValueError):
        message_edit(reg_dict1['token'], -1000, "test")
    with pytest.raises(ValueError):
        message_edit(reg_dict1['token'], 100000000, "test")

##############################
#     message_react Tests    #
##############################

def test_message_react_simple():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    channel_1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], channel_1['channel_id'])
    channel_join(reg_dict3['token'], channel_1['channel_id'])

    message_send(reg_dict1['token'], channel_1['channel_id'], "Message 0")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Oof")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Ouch")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Owie")

    channel_2 = channels_create(reg_dict1['token'], 'PCSoc', True)
    channel_join(reg_dict2['token'], channel_2['channel_id'])

    message_send(reg_dict2['token'], channel_2['channel_id'], "Oof")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Ouch")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Owie")
    # SETUP END

    # Multiple reactions on same message works
    message_react(reg_dict1['token'], 1, 1)
    message_react(reg_dict1['token'], 1, 2)
    message_react(reg_dict1['token'], 1, 3)

    # Those same reactions still work on different message
    message_react(reg_dict1['token'], 2, 1)
    message_react(reg_dict1['token'], 2, 2)
    message_react(reg_dict1['token'], 2, 3)
    
    # Different users can react to same message
    message_react(reg_dict2['token'], 1, 4)
    message_react(reg_dict2['token'], 2, 4)
    message_react(reg_dict2['token'], 3, 4)

    # Reacts work across channels (messages from channel_2)
    message_react(reg_dict2['token'], 4, 1)
    message_react(reg_dict2['token'], 5, 2)
    message_react(reg_dict2['token'], 6, 3)
    message_react(reg_dict1['token'], 4, 4)
    message_react(reg_dict1['token'], 5, 5)
    message_react(reg_dict1['token'], 6, 6)

def test_message_react_message_invalid():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    channel_1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], channel_1['channel_id'])
    channel_join(reg_dict3['token'], channel_1['channel_id'])
    
    message_send(reg_dict1['token'], channel_1['channel_id'], "Message 0")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Oof")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Ouch")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Owie")

    channel_2 = channels_create(reg_dict1['token'], 'PCSoc', True)
    channel_join(reg_dict2['token'], channel_2['channel_id'])

    message_send(reg_dict2['token'], channel_2['channel_id'], "Oof")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Ouch")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Owie")
    # SETUP END
    # Invalid message ids are negative and not currently in the channel
    with pytest.raises(ValueError):
        message_react(reg_dict1['token'], -1, 1)
    with pytest.raises(ValueError):
        message_react(reg_dict1['token'], -101010, 1)
    with pytest.raises(ValueError):
        message_react(reg_dict1['token'], 100000, 1)

    # Those same ids still fail irrespective of user/admin
    with pytest.raises(ValueError):
        message_react(reg_dict2['token'], -1, 1)
    with pytest.raises(ValueError):
        message_react(reg_dict2['token'], -101010, 1)
    with pytest.raises(ValueError):
        message_react(reg_dict2['token'], 100000, 1)
    with pytest.raises(ValueError):
        message_react(reg_dict3['token'], -1, 1)
    with pytest.raises(ValueError):
        message_react(reg_dict3['token'], -101010, 1)
    with pytest.raises(ValueError):
        message_react(reg_dict3['token'], 100000, 1)

    # Invalid message won't have the react when it eventually gets created
    # Currently 6 messages
    with pytest.raises(ValueError):
        message_react(reg_dict1['token'], 7, 1)
    message_send(reg_dict1['token'], channel_1['channel_id'], "Message 7")
    message_react(reg_dict1['token'], 7, 1) # Will not fail

    # A deleted message is an invalid id
    message_react(reg_dict1['token'], 7, 2) # Will not fail
    message_remove(reg_dict1['token'], 7)
    with pytest.raises(ValueError):
        message_react(reg_dict1['token'], 7, 3)

    # Message id invalid when user not in the channel
    message_send(reg_dict2['token'], channel_2['channel_id'], "Message 8")
    message_react(reg_dict1['token'], 8, 1)
    message_react(reg_dict2['token'], 8, 2)
    with pytest.raises(ValueError):
        message_react(reg_dict3['token'], 8, 3)

def test_message_react_react_invalid():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    channel_1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], channel_1['channel_id'])
    channel_join(reg_dict3['token'], channel_1['channel_id'])
    
    message_send(reg_dict1['token'], channel_1['channel_id'], "Message 0")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Oof")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Ouch")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Owie")

    channel_2 = channels_create(reg_dict1['token'], 'PCSoc', True)
    channel_join(reg_dict2['token'], channel_2['channel_id'])

    message_send(reg_dict2['token'], channel_2['channel_id'], "Oof")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Ouch")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Owie")
    # SETUP END

    # React id is invalid as a negative, and doesn't change depending on user
    with pytest.raises(ValueError):
        message_react(reg_dict1['token'], 1, -1)
    with pytest.raises(ValueError):
        message_react(reg_dict1['token'], 2, -912929)
    with pytest.raises(ValueError):
        message_react(reg_dict1['token'], 3, -101010100)
    with pytest.raises(ValueError):
        message_react(reg_dict2['token'], 4, -10)
    with pytest.raises(ValueError):
        message_react(reg_dict3['token'], 5, -42)
    # Can't possibly be 200000000 reacts in this simple created channel
    with pytest.raises(ValueError):
        message_react(reg_dict1['token'], 1, 200000000000)
    with pytest.raises(ValueError):
        message_react(reg_dict1['token'], 2, 200000000000)
    with pytest.raises(ValueError):
        message_react(reg_dict1['token'], 3, 200000000000)
    with pytest.raises(ValueError):
        message_react(reg_dict2['token'], 4, 200000000000)
    with pytest.raises(ValueError):
        message_react(reg_dict3['token'], 5, 200000000000)
    

def test_message_react_message_already_reacted():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    channel_1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], channel_1['channel_id'])
    channel_join(reg_dict3['token'], channel_1['channel_id'])
    
    message_send(reg_dict1['token'], channel_1['channel_id'], "Message 0")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Oof")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Ouch")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Owie")
    # SETUP END
    # Message already reacted to, still fails with different users
    message_react(reg_dict1['token'], 1, 1)
    with pytest.raises(ValueError):
        message_react(reg_dict1['token'], 1, 1)
    with pytest.raises(ValueError):
        message_react(reg_dict2['token'], 1, 1)
    with pytest.raises(ValueError):
        message_react(reg_dict3['token'], 1, 1)
    
    message_react(reg_dict1['token'], 2, 1)
    message_react(reg_dict1['token'], 2, 2)
    with pytest.raises(ValueError):
        message_react(reg_dict1['token'], 2, 1)
    with pytest.raises(ValueError):
        message_react(reg_dict2['token'], 2, 2)
    message_react(reg_dict3['token'], 2, 3)

##############################
#    message_unreact Tests   #
##############################

def test_message_unreact_simple():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    channel_1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], channel_1['channel_id'])
    channel_join(reg_dict3['token'], channel_1['channel_id'])

    message_send(reg_dict1['token'], channel_1['channel_id'], "Message 0")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Oof")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Ouch")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Owie")

    channel_2 = channels_create(reg_dict1['token'], 'PCSoc', True)
    channel_join(reg_dict2['token'], channel_2['channel_id'])

    message_send(reg_dict2['token'], channel_2['channel_id'], "Oof")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Ouch")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Owie")
    # SETUP END

    # Reactions can be removed right after adding
    message_react(reg_dict1['token'], 1, 1)
    message_unreact(reg_dict1['token'], 1, 1)
    message_react(reg_dict1['token'], 1, 2)
    message_unreact(reg_dict1['token'], 1, 2)
    message_react(reg_dict1['token'], 1, 3)
    message_unreact(reg_dict1['token'], 1, 2)

    # Those same reactions can be readded and removed all at once
    message_react(reg_dict1['token'], 1, 1)
    message_react(reg_dict1['token'], 1, 2)
    message_react(reg_dict1['token'], 1, 3)
    message_unreact(reg_dict1['token'], 1, 1)
    message_unreact(reg_dict1['token'], 1, 2)
    message_unreact(reg_dict1['token'], 1, 3)
    
    # Admins can unreact anyones reactions
    message_react(reg_dict2['token'], 1, 4)
    message_react(reg_dict2['token'], 2, 4)
    message_react(reg_dict2['token'], 3, 4)
    message_unreact(reg_dict1['token'], 1, 4)
    message_unreact(reg_dict1['token'], 2, 4)
    message_unreact(reg_dict1['token'], 3, 4)

    # Unreacts work across channels (messages from channel_2)
    message_react(reg_dict2['token'], 4, 1)
    message_react(reg_dict2['token'], 5, 2)
    message_react(reg_dict2['token'], 6, 3)
    message_react(reg_dict1['token'], 4, 4)
    message_react(reg_dict1['token'], 5, 5)
    message_react(reg_dict1['token'], 6, 6)
    message_unreact(reg_dict2['token'], 4, 1)
    message_unreact(reg_dict2['token'], 5, 2)
    message_unreact(reg_dict2['token'], 6, 3)
    message_unreact(reg_dict1['token'], 4, 4)
    message_unreact(reg_dict1['token'], 5, 5)
    message_unreact(reg_dict1['token'], 6, 6)

def test_message_unreact_invalid_message_id():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    channel_1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], channel_1['channel_id'])
    channel_join(reg_dict3['token'], channel_1['channel_id'])

    message_send(reg_dict1['token'], channel_1['channel_id'], "Message 0")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Oof")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Ouch")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Owie")

    channel_2 = channels_create(reg_dict1['token'], 'PCSoc', True)
    channel_join(reg_dict2['token'], channel_2['channel_id'])

    message_send(reg_dict2['token'], channel_2['channel_id'], "Oof")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Ouch")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Owie")
    # SETUP END

    # Message is negative or not created yet
    with pytest.raises(ValueError):
        message_unreact(reg_dict1['token'], -1, 1)
    with pytest.raises(ValueError):
        message_unreact(reg_dict1['token'], -101010, 1)
    with pytest.raises(ValueError):
        message_unreact(reg_dict1['token'], 100000, 1)

    # Those ids still can't be unreacted with different users
    with pytest.raises(ValueError):
        message_unreact(reg_dict2['token'], -1, 1)
    with pytest.raises(ValueError):
        message_unreact(reg_dict2['token'], -101010, 1)
    with pytest.raises(ValueError):
        message_unreact(reg_dict2['token'], 100000, 1)
    with pytest.raises(ValueError):
        message_unreact(reg_dict3['token'], -1, 1)
    with pytest.raises(ValueError):
        message_unreact(reg_dict3['token'], -101010, 1)
    with pytest.raises(ValueError):
        message_unreact(reg_dict3['token'], 100000, 1)

    # A deleted message is invalid
    with pytest.raises(ValueError):
        message_unreact(reg_dict1['token'], 7, 1)
    message_send(reg_dict1['token'], channel_1['channel_id'], "Message 7")
    message_react(reg_dict1['token'], 7, 1) # Will not fail
    message_unreact(reg_dict1['token'], 7, 1) # Will not fail

    # Message id invalid when user not in channel
    message_send(reg_dict2['token'], channel_2['channel_id'], "Message 8")
    message_react(reg_dict1['token'], 8, 1)
    message_react(reg_dict2['token'], 8, 2)
    with pytest.raises(ValueError):
        message_unreact(reg_dict3['token'], 8, 2)

    
def test_message_unreact_invalid_react_id():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    channel_1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], channel_1['channel_id'])
    channel_join(reg_dict3['token'], channel_1['channel_id'])

    message_send(reg_dict1['token'], channel_1['channel_id'], "Message 0")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Oof")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Ouch")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Owie")

    channel_2 = channels_create(reg_dict1['token'], 'PCSoc', True)
    channel_join(reg_dict2['token'], channel_2['channel_id'])

    message_send(reg_dict2['token'], channel_2['channel_id'], "Oof")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Ouch")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Owie")
    # SETUP END
    
    # React id is invalid as a negative, and doesn't change depending on user
    with pytest.raises(ValueError):
        message_unreact(reg_dict1['token'], 1, -1)
    with pytest.raises(ValueError):
        message_unreact(reg_dict1['token'], 2, -912929)
    with pytest.raises(ValueError):
        message_unreact(reg_dict1['token'], 3, -101010100)
    with pytest.raises(ValueError):
        message_unreact(reg_dict2['token'], 4, -10)
    with pytest.raises(ValueError):
        message_unreact(reg_dict3['token'], 5, -42)
    # Can't possibly be 200000000 reacts in this simple created channel
    with pytest.raises(ValueError):
        message_unreact(reg_dict1['token'], 1, 200000000000)
    with pytest.raises(ValueError):
        message_unreact(reg_dict1['token'], 2, 200000000000)
    with pytest.raises(ValueError):
        message_unreact(reg_dict1['token'], 3, 200000000000)
    with pytest.raises(ValueError):
        message_unreact(reg_dict2['token'], 4, 200000000000)
    with pytest.raises(ValueError):
        message_unreact(reg_dict3['token'], 5, 200000000000)

def test_message_unreact_already_no_reaction():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    channel_1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], channel_1['channel_id'])
    channel_join(reg_dict3['token'], channel_1['channel_id'])

    message_send(reg_dict1['token'], channel_1['channel_id'], "Message 0")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Oof")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Ouch")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Owie")

    channel_2 = channels_create(reg_dict1['token'], 'PCSoc', True)
    channel_join(reg_dict2['token'], channel_2['channel_id'])

    message_send(reg_dict2['token'], channel_2['channel_id'], "Oof")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Ouch")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Owie")
    # SETUP END
    # Messages having no reactions to begin with
    with pytest.raises(ValueError):
        message_unreact(reg_dict1['token'], 1, 1)
    with pytest.raises(ValueError):
        message_unreact(reg_dict1['token'], 1, 2)
    with pytest.raises(ValueError):
        message_unreact(reg_dict1['token'], 1, 3)
    with pytest.raises(ValueError):
        message_unreact(reg_dict2['token'], 2, 1)
    with pytest.raises(ValueError):
        message_unreact(reg_dict2['token'], 2, 2)
    with pytest.raises(ValueError):
        message_unreact(reg_dict2['token'], 2, 3)

    # Message had reaction, but got unreacted
    message_react(reg_dict1['token'], 1, 1)
    message_unreact(reg_dict1['token'], 1, 1) # won't fail first time
    with pytest.raises(ValueError):
        message_unreact(reg_dict1['token'], 1, 1)
    
    # Can still react and unreact again
    message_react(reg_dict2['token'], 1, 1)
    message_unreact(reg_dict2['token'], 1, 1)
    with pytest.raises(ValueError):
        message_unreact(reg_dict1['token'], 1, 1)

    
##############################
#     message_pin Tests      #
##############################

def test_message_pin_simple():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    channel_1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], channel_1['channel_id'])
    channel_join(reg_dict3['token'], channel_1['channel_id'])

    message_send(reg_dict1['token'], channel_1['channel_id'], "Message 0")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Oof")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Ouch")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Owie")

    channel_2 = channels_create(reg_dict2['token'], 'PCSoc', True)
    channel_join(reg_dict2['token'], channel_2['channel_id'])

    message_send(reg_dict2['token'], channel_2['channel_id'], "Oof")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Ouch")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Owie")
    # SETUP END

    # Can pin messages that have been created in any channel by the admin
    message_pin(reg_dict1['token'], 1)
    message_pin(reg_dict1['token'], 2)
    message_pin(reg_dict1['token'], 3)

    message_pin(reg_dict2['token'], 4)
    message_pin(reg_dict2['token'], 5)
    message_pin(reg_dict2['token'], 6)

    
def test_message_pin_invalid_message():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    channel_1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], channel_1['channel_id'])
    channel_join(reg_dict3['token'], channel_1['channel_id'])

    message_send(reg_dict1['token'], channel_1['channel_id'], "Message 0")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Oof")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Ouch")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Owie")

    channel_2 = channels_create(reg_dict2['token'], 'PCSoc', True)
    channel_join(reg_dict2['token'], channel_2['channel_id'])

    message_send(reg_dict2['token'], channel_2['channel_id'], "Oof")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Ouch")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Owie")
    # SETUP END

    # Invalid message if id is negative or not created yet
    with pytest.raises(ValueError): 
        message_pin(reg_dict1['token'], -1)
    with pytest.raises(ValueError):
        message_pin(reg_dict1['token'], -2)
    with pytest.raises(ValueError):
        message_pin(reg_dict1['token'], -3)
    with pytest.raises(ValueError):
        message_pin(reg_dict1['token'], -30000)
    with pytest.raises(ValueError):
        message_pin(reg_dict1['token'], 200000000)
    
    # Invalid message if message deleted
    with pytest.raises(ValueError):
        message_pin(reg_dict1['token'], 7)
    message_send(reg_dict1['token'], channel_1['channel_id'], "Message 7")
    message_remove(reg_dict1['token'], 7)
    with pytest.raises(ValueError):
        message_pin(reg_dict1['token'], 7)

    # Message won't be pinned upon creation if it was previously invalid
    with pytest.raises(ValueError):
        message_pin(reg_dict1['token'], 8)
    message_send(reg_dict1['token'], channel_1['channel_id'], "Message 8")
    message_pin(reg_dict1['token'], 8) # Won't fail as it shouldn't have been pinned


def test_message_pin_user_not_admin():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    channel_1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], channel_1['channel_id'])
    channel_join(reg_dict3['token'], channel_1['channel_id'])

    message_send(reg_dict1['token'], channel_1['channel_id'], "Message 0")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Oof")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Ouch")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Owie")

    channel_2 = channels_create(reg_dict2['token'], 'PCSoc', True)
    channel_join(reg_dict2['token'], channel_2['channel_id'])

    message_send(reg_dict2['token'], channel_2['channel_id'], "Oof")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Ouch")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Owie")
    # SETUP END

    # Can't pin if the user is not an admin for the message's channel
    with pytest.raises(ValueError):
        message_pin(reg_dict2['token'], 1)
    message_pin(reg_dict1['token'], 1) # user1 is an owner of channel1

    with pytest.raises(ValueError):
        message_pin(reg_dict1['token'], 4)
    message_pin(reg_dict2['token'], 4) # user2 is an owner of the channel2

    # Adding these users as owners should now allow them to pin
    with pytest.raises(ValueError):
        message_pin(reg_dict2['token'], 2)
    channel_addowner(reg_dict1['token'], channel_1['channel_id'], reg_dict2['u_id'])
    message_pin(reg_dict2['token'], 2)

    # And when they lose ownership, their pinned messages should stay pinned
    channel_removeowner(reg_dict1['token'], channel_1['channel_id'], reg_dict2['u_id'])
    with pytest.raises(ValueError):
        message_pin(reg_dict1['token'], 2)
    # But they can't pin anymore
    with pytest.raises(ValueError):
        message_pin(reg_dict2['token'], 3)


def test_message_pin_already_pinned():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    channel_1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], channel_1['channel_id'])
    channel_join(reg_dict3['token'], channel_1['channel_id'])

    message_send(reg_dict1['token'], channel_1['channel_id'], "Message 0")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Oof")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Ouch")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Owie")

    channel_2 = channels_create(reg_dict2['token'], 'PCSoc', True)
    channel_join(reg_dict2['token'], channel_2['channel_id'])

    message_send(reg_dict2['token'], channel_2['channel_id'], "Oof")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Ouch")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Owie")
    # SETUP END

    # Can't pin already pinned message
    message_pin(reg_dict1['token'], 1)
    with pytest.raises(ValueError):
        message_pin(reg_dict1['token'], 1)
    
    message_pin(reg_dict2['token'], 4)
    with pytest.raises(ValueError):
        message_pin(reg_dict2['token'], 4)

    message_pin(reg_dict2['token'], 5)
    with pytest.raises(ValueError):
        message_pin(reg_dict2['token'], 5)

    # An unpinned message is repinnable
    message_unpin(reg_dict1['token'], 1)
    message_pin(reg_dict1['token'], 1)
    with pytest.raises(ValueError):
        message_pin(reg_dict1['token'], 1)

    # A message pinned by another owner will still be unpinnable
    message_pin(reg_dict1['token'], 1)
    channel_addowner(reg_dict1['token'], channel_1['channel_id'], reg_dict2['u_id'])
    with pytest.raises(ValueError):
        message_pin(reg_dict2['token'], 1)

    

def test_message_pin_not_in_channel():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    channel_1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], channel_1['channel_id'])
    channel_join(reg_dict3['token'], channel_1['channel_id'])

    message_send(reg_dict1['token'], channel_1['channel_id'], "Message 0")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Oof")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Ouch")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Owie")

    channel_2 = channels_create(reg_dict2['token'], 'PCSoc', True)
    channel_join(reg_dict2['token'], channel_2['channel_id'])

    message_send(reg_dict2['token'], channel_2['channel_id'], "Oof")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Ouch")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Owie")
    # SETUP END

    # Can't pin a message if the user isn't even part of the channel
    message_pin(reg_dict1['token'], 1)
    with pytest.raises(ValueError):
        message_pin(reg_dict1['token'], 4)
    message_pin(reg_dict2['token'], 4)
    with pytest.raises(ValueError):
        message_pin(reg_dict3['token'], 5)
    message_pin(reg_dict2['token'], 5)

    # A user who joins the channel still can't pin until they become an owner
    channel_join(reg_dict1['token'], channel_2['channel_id'])
    with pytest.raises(ValueError):
        message_pin(reg_dict1['token'], 6)
    channel_addowner(reg_dict2['token'], channel_2['channel_id'], reg_dict1['u_id'])
    message_pin(reg_dict1['token'], 6)

##############################
#     message_unpin Tests    #
##############################

def test_message_unpin_simple():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    channel_1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], channel_1['channel_id'])
    channel_join(reg_dict3['token'], channel_1['channel_id'])

    message_send(reg_dict1['token'], channel_1['channel_id'], "Message 0")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Oof")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Ouch")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Owie")

    channel_2 = channels_create(reg_dict2['token'], 'PCSoc', True)
    channel_join(reg_dict2['token'], channel_2['channel_id'])

    message_send(reg_dict2['token'], channel_2['channel_id'], "Oof")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Ouch")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Owie")
    # SETUP END

    # Messages can be unpinned by the owners of the channel
    message_pin(reg_dict1['token'], 1)
    message_pin(reg_dict1['token'], 2)
    message_pin(reg_dict1['token'], 3)
    message_unpin(reg_dict1['token'], 1)
    message_unpin(reg_dict1['token'], 2)
    message_unpin(reg_dict1['token'], 3)

    message_pin(reg_dict2['token'], 4)
    message_pin(reg_dict2['token'], 5)
    message_pin(reg_dict2['token'], 6)
    message_unpin(reg_dict2['token'], 4)
    message_unpin(reg_dict2['token'], 5)
    message_unpin(reg_dict2['token'], 6)


def test_message_unpin_invalid_message():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    channel_1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], channel_1['channel_id'])
    channel_join(reg_dict3['token'], channel_1['channel_id'])

    message_send(reg_dict1['token'], channel_1['channel_id'], "Message 0")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Oof")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Ouch")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Owie")

    channel_2 = channels_create(reg_dict2['token'], 'PCSoc', True)
    channel_join(reg_dict2['token'], channel_2['channel_id'])

    message_send(reg_dict2['token'], channel_2['channel_id'], "Oof")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Ouch")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Owie")
    # SETUP END

    # Invalid message if the id is negative or not created yet
    with pytest.raises(ValueError): 
        message_unpin(reg_dict1['token'], -1)
    with pytest.raises(ValueError):
        message_unpin(reg_dict1['token'], -2)
    with pytest.raises(ValueError):
        message_unpin(reg_dict1['token'], -3)
    with pytest.raises(ValueError):
        message_unpin(reg_dict1['token'], -30000)
    with pytest.raises(ValueError):
        message_unpin(reg_dict1['token'], 200000000)
    
    # Invalid message if message deleted
    with pytest.raises(ValueError):
        message_unpin(reg_dict1['token'], 7)
    message_send(reg_dict1['token'], channel_1['channel_id'], "Message 7")
    message_pin(reg_dict1['token'], 7)
    message_unpin(reg_dict1['token'], 7)
    message_pin(reg_dict1['token'], 7)
    message_remove(reg_dict1['token'], 7)
    with pytest.raises(ValueError):
        message_unpin(reg_dict1['token'], 7)

def test_message_unpin_user_not_admin():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    channel_1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], channel_1['channel_id'])
    channel_join(reg_dict3['token'], channel_1['channel_id'])

    message_send(reg_dict1['token'], channel_1['channel_id'], "Message 0")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Oof")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Ouch")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Owie")

    channel_2 = channels_create(reg_dict2['token'], 'PCSoc', True)
    channel_join(reg_dict2['token'], channel_2['channel_id'])

    message_send(reg_dict2['token'], channel_2['channel_id'], "Oof")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Ouch")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Owie")
    # SETUP END
    message_pin(reg_dict1['token'], 1)
    # Can't unpin if the user is not an admin for the message's channel
    with pytest.raises(ValueError):
        message_unpin(reg_dict2['token'], 1)
    message_unpin(reg_dict1['token'], 1) # user1 is an owner of channel1

    message_pin(reg_dict2['token'], 4)
    with pytest.raises(ValueError):
        message_unpin(reg_dict1['token'], 4)
    message_unpin(reg_dict2['token'], 4) # user2 is an owner of channel2

    # Adding users as owners/admins should allow them to unpin
    message_pin(reg_dict1['token'], 2)
    with pytest.raises(ValueError):
        message_unpin(reg_dict2['token'], 2)
    channel_addowner(reg_dict1['token'], channel_1['channel_id'], reg_dict2['u_id'])
    message_unpin(reg_dict2['token'], 2)

    # After losing ownership their unpinned messages stay unpinned
    channel_removeowner(reg_dict1['token'], channel_1['channel_id'], reg_dict2['u_id'])
    with pytest.raises(ValueError):
        message_unpin(reg_dict1['token'], 2)
    # But they also can't unpin anymore messages
    message_pin(reg_dict1['token'], 3)
    with pytest.raises(ValueError):
        message_unpin(reg_dict2['token'], 3)

def test_message_unpin_already_unpinned():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    channel_1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], channel_1['channel_id'])
    channel_join(reg_dict3['token'], channel_1['channel_id'])

    message_send(reg_dict1['token'], channel_1['channel_id'], "Message 0")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Oof")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Ouch")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Owie")

    channel_2 = channels_create(reg_dict2['token'], 'PCSoc', True)
    channel_join(reg_dict2['token'], channel_2['channel_id'])

    message_send(reg_dict2['token'], channel_2['channel_id'], "Oof")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Ouch")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Owie")
    # SETUP END

    # Can't unpin a messaged that's unpinned
    with pytest.raises(ValueError):
        message_unpin(reg_dict1['token'], 1)
    message_pin(reg_dict1['token'], 1)
    message_unpin(reg_dict1['token'], 1)
    with pytest.raises(ValueError):
        message_unpin(reg_dict1['token'], 1)
    
    with pytest.raises(ValueError):
        message_unpin(reg_dict2['token'], 4)
    message_pin(reg_dict2['token'], 4)
    message_unpin(reg_dict2['token'], 4)
    with pytest.raises(ValueError):
        message_unpin(reg_dict2['token'], 4)

    with pytest.raises(ValueError):
        message_unpin(reg_dict2['token'], 5)
    message_pin(reg_dict2['token'], 5)
    message_unpin(reg_dict2['token'], 5)
    with pytest.raises(ValueError):
        message_unpin(reg_dict2['token'], 5)

    # An unpinned message is repinnable
    with pytest.raises(ValueError):
        message_unpin(reg_dict1['token'], 3)
    message_pin(reg_dict1['token'], 3)
    with pytest.raises(ValueError):
        message_pin(reg_dict1['token'], 1)
    message_unpin(reg_dict1['token'], 3)
    with pytest.raises(ValueError):
        message_unpin(reg_dict1['token'], 3)

    # A message unpinned by another owner can't be unpinned again
    message_pin(reg_dict1['token'], 1)
    channel_addowner(reg_dict1['token'], channel_1['channel_id'], reg_dict2['u_id'])
    message_unpin(reg_dict2['token'], 1)
    with pytest.raises(ValueError):
        message_unpin(reg_dict1['token'], 1)

def test_message_unpin_not_in_channel():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    channel_1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], channel_1['channel_id'])
    channel_join(reg_dict3['token'], channel_1['channel_id'])

    message_send(reg_dict1['token'], channel_1['channel_id'], "Message 0")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Oof")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Ouch")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Owie")

    channel_2 = channels_create(reg_dict2['token'], 'PCSoc', True)
    channel_join(reg_dict2['token'], channel_2['channel_id'])

    message_send(reg_dict2['token'], channel_2['channel_id'], "Oof")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Ouch")
    message_send(reg_dict2['token'], channel_2['channel_id'], "Owie")
    # SETUP END

    # Can't unpin a message if the user isn't in the channel
    message_pin(reg_dict1['token'], 1)
    message_unpin(reg_dict1['token'], 1)
    with pytest.raises(ValueError):
        message_unpin(reg_dict1['token'], 4)
    message_pin(reg_dict2['token'], 4)
    with pytest.raises(ValueError):
        message_unpin(reg_dict3['token'], 4)
    message_unpin(reg_dict2['token'], 4)

    # A user who joins the channel still can't unpin until they become an owner
    message_pin(reg_dict2['token'], 6)
    channel_join(reg_dict1['token'], channel_2['channel_id'])
    with pytest.raises(ValueError):
        message_unpin(reg_dict1['token'], 6)
    channel_addowner(reg_dict2['token'], channel_2['channel_id'], reg_dict1['u_id'])
    message_unpin(reg_dict2['token'], 6)
    