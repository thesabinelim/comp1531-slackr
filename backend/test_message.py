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
from .db import (db_get_channel_by_channel_id,reset_data,get_data,db_get_message_by_message_id,db_get_all_channels,db_get_channel_by_channel_id,db_get_message_by_message_id)
from .channel import (
    channel_join, channel_invite, channel_leave, channel_addowner,
    channel_removeowner, channel_messages
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
            'u_id': reg_dict1['u_id'],
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
            'u_id': reg_dict2['u_id'],
            'message': 'Ouch',
            'time_created': now_plus_hour,
            'reacts': [],
            'is_pinned': False
        },
        {
            'message_id': message_dict1['message_id'],
            'u_id': reg_dict1['u_id'],
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
            'u_id': reg_dict3['u_id'],
            'message': 'Owie',
            'time_created': now_plus_days,
            'reacts': [],
            'is_pinned': False
        },
        {
            'message_id': message_dict2['message_id'],
            'u_id': reg_dict2['u_id'],
            'message': 'Ouch',
            'time_created': now_plus_hour,
            'reacts': [],
            'is_pinned': False
        },
        {
            'message_id': message_dict1['message_id'],
            'u_id': reg_dict1['u_id'],
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
    reset_data()

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
    assert channel_message3['message'] == 'Owie'
    
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
    reset_data()

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
        message_remove(reg_dict2['token'], message_dict2['message_id'])
    with pytest.raises(AccessError):
        message_remove(reg_dict1['token'], message_dict1['message_id'])

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
    assert message_remove(reg_dict1['token'], message_dict4['message_id']) == {}


######################
# message_edit Tests #
######################

def test_message_edit_simple():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    create_dict2 = channels_create(reg_dict2['token'], 'PCSoc', False)

    message_dict1 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Oof")
    message_dict2 = message_send(reg_dict2['token'], create_dict2['channel_id'], "Ouch")
    # SETUP END

    assert message_edit(reg_dict1['token'], message_dict1['message_id'], "Boom") == {}
    assert message_edit(reg_dict2['token'], message_dict2['message_id'], "Pow") == {}

def test_message_edit_same_text():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)

    message_dict1 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Oof")
    # SETUP END

    assert message_edit(reg_dict1['token'], message_dict1['message_id'], "Oof") == {}

def test_message_edit_multiple_times():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)

    message_dict1 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Oof")
    # SETUP END

    assert message_edit(reg_dict1['token'], message_dict1['message_id'], "Boom") == {}
    assert message_edit(reg_dict1['token'], message_dict1['message_id'], "Pow") == {}
    assert message_edit(reg_dict1['token'], message_dict1['message_id'], "Splat") == {}

def test_message_edit_message_too_long():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    create_dict2 = channels_create(reg_dict2['token'], 'PCSoc', False)

    message_dict1 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Oof")
    message_dict2 = message_send(reg_dict2['token'], create_dict2['channel_id'], "Ouch")
    # SETUP END

    # Messages must still abide by the 1000 char limit
    too_long_msg = "If you take the temperature of a superconductor down to absolute zero (around minus 273.1 centigrade), it ignores gravity and floats. This is a scientific fact and you are welcome to check - google or youtube it. My 9yo son asked why we couldn't freeze a car to -273C and fly in it and I told him that the car would neutralise gravity, not reverse it and the weight of the people in it would make it sink. Also, heat rises so -273C should really sink unless it was in a vacuum which means we wouldn't be able to breath or hear the stereo. You would also need to rug up well. If you take the temperature of a superconductor down to absolute zero (around minus 273.1 centigrade), it ignores gravity and floats. This is a scientific fact and you are welcome to check - google or youtube it. My 9yo son asked why we couldn't freeze a car to -273C and fly in it and I told him that the car would neutralise gravity, not reverse it and the weight of the people in it would make it sink. Also, heat rises so -273C should really sink unless it was in a vacuum which means we wouldn't be able to breath or hear the stereo. You would also need to rug up well."
    with pytest.raises(ValueError):
        message_edit(reg_dict1['token'], message_dict1['message_id'], too_long_msg)
    with pytest.raises(ValueError):
        message_edit(reg_dict2['token'], message_dict2['message_id'], too_long_msg)

def test_message_edit_message_empty():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)

    message_dict1 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Oof")
    message_dict2 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Ouch")
    # SETUP END
    channel1 = db_get_channel_by_channel_id(create_dict1['channel_id'])

    messages1 = db_get_message_by_message_id(message_dict1['message_id'])
    messages2 = db_get_message_by_message_id(message_dict2['message_id'])
    # Empty text means deleting this message
    assert message_edit(reg_dict1['token'], message_dict1['message_id'], "") == {}
    assert not channel1.has_message(messages1)


def test_message_edit_invalid_message_id():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)

    message_dict1 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Oof")
    # SETUP END

    with pytest.raises(ValueError):
        message_edit(reg_dict1['token'], message_dict1['message_id'] + 1, "Boom")
    
    # Invalid message if message deleted
    message_remove(reg_dict1['token'], message_dict1['message_id'])
    with pytest.raises(ValueError):
        message_edit(reg_dict1['token'], message_dict1['message_id'], "Boom")

def test_message_edit_not_in_channel():
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
        message_edit(reg_dict2['token'], message_dict2['message_id'], "Pow")
    with pytest.raises(AccessError):
        message_edit(reg_dict1['token'], message_dict1['message_id'], "Boom")

def test_message_edit_not_sender():
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

    # Message can't be edited by regular user who didn't send the message
    with pytest.raises(AccessError):
        message_edit(reg_dict3['token'], message_dict2['message_id'], "Pow")

    # Message sent by owner of the channel, can't be edited by regular users
    with pytest.raises(AccessError):
        message_edit(reg_dict2['token'], message_dict1['message_id'], "Boom")
    with pytest.raises(AccessError):
        message_edit(reg_dict3['token'], message_dict1['message_id'], "Boom")

    # Regular user gains ability to edit others' messages when they become
    # channel owner, including messages from other channel owners
    channel_addowner(reg_dict1['token'], create_dict1['channel_id'], reg_dict3['u_id'])
    assert message_edit(reg_dict3['token'], message_dict2['message_id'], "Pow") == {}
    assert message_edit(reg_dict3['token'], message_dict1['message_id'], "Boom") == {}

    # Owners of one channel can't edit others' messages in other channels they
    # aren't owner of
    with pytest.raises(AccessError):
        message_edit(reg_dict3['token'], message_dict3['message_id'], "Splat")
    with pytest.raises(AccessError):
        message_edit(reg_dict3['token'], message_dict4['message_id'], "Kablam")

    # Unless they're a Slackr admin/owner
    assert message_remove(reg_dict1['token'], message_dict4['message_id']) == {}

#######################
# message_react Tests #
#######################

def test_message_react_simple():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], create_dict1['channel_id'])
    channel_join(reg_dict3['token'], create_dict1['channel_id'])

    message_dict1 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Oof")
    # SETUP END

    assert message_react(reg_dict1['token'], message_dict1['message_id'], 1) == {}
    assert message_react(reg_dict1['token'], message_dict1['message_id'], 2) == {}
    assert message_react(reg_dict1['token'], message_dict1['message_id'], 3) == {}

    assert message_react(reg_dict2['token'], message_dict1['message_id'], 1) == {}
    assert message_react(reg_dict2['token'], message_dict1['message_id'], 2) == {}

    assert message_react(reg_dict3['token'], message_dict1['message_id'], 1) == {}

    assert channel_messages(reg_dict1['token'], create_dict1['channel_id'], 0)['messages'][0]['reacts'] == [
        {
            'react_id': 1,
            'u_ids': [reg_dict1['u_id'], reg_dict2['u_id'], reg_dict3['u_id']],
            'is_this_user_reacted': True
        },
        {
            'react_id': 2,
            'u_ids': [reg_dict1['u_id'], reg_dict2['u_id']],
            'is_this_user_reacted': True
        },
        {
            'react_id': 3,
            'u_ids': [reg_dict1['u_id']],
            'is_this_user_reacted': True
        }
    ]

def test_message_react_message_invalid_message_id():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    
    message_dict1 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Oof")
    # SETUP END

    with pytest.raises(ValueError):
        message_react(reg_dict1['token'], message_dict1['message_id'] + 1, 1)

    # A deleted message is an invalid id
    message_remove(reg_dict1['token'], message_dict1['message_id'])
    with pytest.raises(ValueError):
        message_react(reg_dict1['token'], message_dict1['message_id'], 1)

def test_message_react_not_in_channel():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    
    message_dict1 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Oof")
    # SETUP END

    with pytest.raises(ValueError):
        message_react(reg_dict2['token'], message_dict1['message_id'], 1)
    with pytest.raises(ValueError):
        message_react(reg_dict3['token'], message_dict1['message_id'], 1)

def test_message_react_message_already_reacted():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], create_dict1['channel_id'])
    channel_join(reg_dict3['token'], create_dict1['channel_id'])

    message_dict1 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Oof")
    # SETUP END

    assert message_react(reg_dict1['token'], message_dict1['message_id'], 1) == {}
    assert message_react(reg_dict1['token'], message_dict1['message_id'], 2) == {}
    assert message_react(reg_dict1['token'], message_dict1['message_id'], 3) == {}

    assert message_react(reg_dict2['token'], message_dict1['message_id'], 1) == {}
    assert message_react(reg_dict2['token'], message_dict1['message_id'], 2) == {}

    assert message_react(reg_dict3['token'], message_dict1['message_id'], 1) == {}

    # Reacting again
    with pytest.raises(ValueError):
        message_react(reg_dict1['token'], message_dict1['message_id'], 1)
    with pytest.raises(ValueError):
        message_react(reg_dict1['token'], message_dict1['message_id'], 2)
    with pytest.raises(ValueError):
        message_react(reg_dict1['token'], message_dict1['message_id'], 3)

    with pytest.raises(ValueError):
        message_react(reg_dict2['token'], message_dict1['message_id'], 1)
    with pytest.raises(ValueError):
        message_react(reg_dict2['token'], message_dict1['message_id'], 2)

    with pytest.raises(ValueError):
        message_react(reg_dict3['token'], message_dict1['message_id'], 1)

#########################
# message_unreact Tests #
#########################

def test_message_unreact_simple():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], create_dict1['channel_id'])
    channel_join(reg_dict3['token'], create_dict1['channel_id'])

    message_dict1 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Oof")

    message_react(reg_dict1['token'], message_dict1['message_id'], 1)
    message_react(reg_dict1['token'], message_dict1['message_id'], 2)
    message_react(reg_dict1['token'], message_dict1['message_id'], 3)

    message_react(reg_dict2['token'], message_dict1['message_id'], 1)
    message_react(reg_dict2['token'], message_dict1['message_id'], 2)

    message_react(reg_dict3['token'], message_dict1['message_id'], 1)
    # SETUP END

    assert message_unreact(reg_dict1['token'], message_dict1['message_id'], 2) == {}
    assert message_unreact(reg_dict1['token'], message_dict1['message_id'], 3) == {}

    assert message_unreact(reg_dict2['token'], message_dict1['message_id'], 1) == {}

    assert channel_messages(reg_dict1['token'], create_dict1['channel_id'], 0)['messages'][0]['reacts'] == [
        {
            'react_id': 1,
            'u_ids': [reg_dict1['u_id'], reg_dict3['u_id']],
            'is_this_user_reacted': True
        },
        {
            'react_id': 2,
            'u_ids': [reg_dict2['u_id']],
            'is_this_user_reacted': False
        }
    ]

def test_message_unreact_message_invalid_message_id():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    
    message_dict1 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Oof")

    message_react(reg_dict1['token'], message_dict1['message_id'], 1)
    # SETUP END

    with pytest.raises(ValueError):
        message_unreact(reg_dict1['token'], message_dict1['message_id'] + 1, 1)

    # A deleted message is an invalid id
    message_remove(reg_dict1['token'], message_dict1['message_id'])
    with pytest.raises(ValueError):
        message_unreact(reg_dict1['token'], message_dict1['message_id'], 1)

def test_message_unreact_not_in_channel():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    
    message_dict1 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Oof")

    channel_join(reg_dict2['token'], create_dict1['channel_id'])
    message_react(reg_dict2['token'], message_dict1['message_id'], 1)
    channel_leave(reg_dict2['token'], create_dict1['channel_id'])

    channel_join(reg_dict3['token'], create_dict1['channel_id'])
    message_react(reg_dict3['token'], message_dict1['message_id'], 1)
    channel_leave(reg_dict3['token'], create_dict1['channel_id'])
    # SETUP END

    with pytest.raises(ValueError):
        message_unreact(reg_dict2['token'], message_dict1['message_id'], 1)
    with pytest.raises(ValueError):
        message_unreact(reg_dict3['token'], message_dict1['message_id'], 1)

def test_message_unreact_message_already_unreacted():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], create_dict1['channel_id'])
    channel_join(reg_dict3['token'], create_dict1['channel_id'])

    message_dict1 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Oof")

    message_react(reg_dict1['token'], message_dict1['message_id'], 1)
    message_react(reg_dict1['token'], message_dict1['message_id'], 2)
    message_react(reg_dict1['token'], message_dict1['message_id'], 3)

    message_react(reg_dict2['token'], message_dict1['message_id'], 1)
    message_react(reg_dict2['token'], message_dict1['message_id'], 2)

    message_react(reg_dict3['token'], message_dict1['message_id'], 1)
    # SETUP END

    assert message_unreact(reg_dict1['token'], message_dict1['message_id'], 1) == {}
    assert message_unreact(reg_dict1['token'], message_dict1['message_id'], 2) == {}
    assert message_unreact(reg_dict1['token'], message_dict1['message_id'], 3) == {}

    assert message_unreact(reg_dict2['token'], message_dict1['message_id'], 1) == {}
    assert message_unreact(reg_dict2['token'], message_dict1['message_id'], 2) == {}

    assert message_unreact(reg_dict3['token'], message_dict1['message_id'], 1) == {}

    # Reacting again
    with pytest.raises(ValueError):
        message_unreact(reg_dict1['token'], message_dict1['message_id'], 1)
    with pytest.raises(ValueError):
        message_unreact(reg_dict1['token'], message_dict1['message_id'], 2)
    with pytest.raises(ValueError):
        message_unreact(reg_dict1['token'], message_dict1['message_id'], 3)

    with pytest.raises(ValueError):
        message_unreact(reg_dict2['token'], message_dict1['message_id'], 1)
    with pytest.raises(ValueError):
        message_unreact(reg_dict2['token'], message_dict1['message_id'], 2)

    with pytest.raises(ValueError):
        message_unreact(reg_dict3['token'], message_dict1['message_id'], 1)

#####################
# message_pin Tests #
#####################

def test_message_pin_simple():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    create_dict2 = channels_create(reg_dict2['token'], 'PCSoc', False)
    create_dict3 = channels_create(reg_dict3['token'], 'Steam', True)

    channel_invite(reg_dict2['token'], create_dict2['channel_id'], reg_dict1['u_id'])

    message_dict1 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Oof")
    message_dict2 = message_send(reg_dict2['token'], create_dict2['channel_id'], "Ouch")
    message_dict3 = message_send(reg_dict3['token'], create_dict3['channel_id'], "Owie")
    # SETUP END

    assert message_pin(reg_dict1['token'], message_dict1['message_id']) == {}
    assert message_pin(reg_dict2['token'], message_dict2['message_id']) == {}
    assert message_pin(reg_dict3['token'], message_dict3['message_id']) == {}

def test_message_pin_not_admin():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], create_dict1['channel_id'])
    channel_join(reg_dict3['token'], create_dict1['channel_id'])

    message_dict1 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Message 0")
    message_dict2 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Oof")
    message_dict3 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Ouch")
    message_dict4 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Owie")

    create_dict2 = channels_create(reg_dict2['token'], 'PCSoc', True)
    channel_join(reg_dict2['token'], create_dict2['channel_id'])
    # SETUP END

    # Can't pin if the user is not an owner of the message's channel
    with pytest.raises(ValueError):
        message_pin(reg_dict2['token'], message_dict1['message_id'])
    assert message_pin(reg_dict1['token'], message_dict1['message_id']) == {}

    with pytest.raises(ValueError):
        message_pin(reg_dict3['token'], message_dict4['message_id'])
    assert message_pin(reg_dict1['token'], message_dict4['message_id']) == {}

    # Adding these users as owners should now allow them to pin
    with pytest.raises(ValueError):
        message_pin(reg_dict2['token'], message_dict2['message_id'])
    channel_addowner(reg_dict1['token'], create_dict1['channel_id'], reg_dict2['u_id'])
    assert message_pin(reg_dict2['token'], message_dict2['message_id']) == {}

    # And when they lose ownership, their pinned messages should stay pinned
    channel_removeowner(reg_dict1['token'], create_dict1['channel_id'], reg_dict2['u_id'])
    with pytest.raises(ValueError):
        message_pin(reg_dict1['token'], message_dict2['message_id'])

    # But they can't pin anymore
    with pytest.raises(ValueError):
        message_pin(reg_dict2['token'], message_dict3['message_id'])

def test_message_pin_invalid_message():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)

    message_dict1 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Oof")
    # SETUP END

    # Invalid message id
    with pytest.raises(ValueError):
        message_pin(reg_dict1['token'], message_dict1['message_id'] + 1)
    
    # Invalid message if message deleted
    message_remove(reg_dict1['token'], message_dict1['message_id'])
    with pytest.raises(ValueError):
        message_pin(reg_dict1['token'], message_dict1['message_id'])

def test_message_pin_already_pinned():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)

    message_dict1 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Oof")
    # SETUP END

    assert message_pin(reg_dict1['token'], message_dict1['message_id']) == {}

    with pytest.raises(ValueError):
        message_pin(reg_dict1['token'], message_dict1['message_id'])

def test_message_pin_not_in_channel():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    create_dict2 = channels_create(reg_dict2['token'], 'PCSoc', False)

    message_dict1 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Oof")
    message_dict2 = message_send(reg_dict2['token'], create_dict2['channel_id'], "Ouch")
    # SETUP END

    with pytest.raises(AccessError):
        message_pin(reg_dict1['token'], message_dict2['message_id'])
    with pytest.raises(AccessError):
        message_pin(reg_dict2['token'], message_dict1['message_id'])

#######################
# message_unpin Tests #
#######################

def test_message_unpin_simple():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    create_dict2 = channels_create(reg_dict2['token'], 'PCSoc', False)
    create_dict3 = channels_create(reg_dict3['token'], 'Steam', True)

    channel_invite(reg_dict2['token'], create_dict2['channel_id'], reg_dict1['u_id'])

    message_dict1 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Oof")
    message_dict2 = message_send(reg_dict2['token'], create_dict2['channel_id'], "Ouch")
    message_dict3 = message_send(reg_dict3['token'], create_dict3['channel_id'], "Owie")

    message_pin(reg_dict1['token'], message_dict1['message_id'])
    message_pin(reg_dict2['token'], message_dict2['message_id'])
    message_pin(reg_dict3['token'], message_dict3['message_id'])
    # SETUP END

    assert message_unpin(reg_dict1['token'], message_dict1['message_id']) == {}
    assert message_unpin(reg_dict2['token'], message_dict2['message_id']) == {}
    assert message_unpin(reg_dict3['token'], message_dict3['message_id']) == {}

def test_message_unpin_invalid_message():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)

    message_dict1 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Oof")

    message_pin(reg_dict1['token'], message_dict1['message_id'])
    # SETUP END

    # Invalid message id
    with pytest.raises(ValueError): 
        message_unpin(reg_dict1['token'], message_dict1['message_id'] + 1)

    # Invalid message if message deleted
    message_remove(reg_dict1['token'], message_dict1['message_id'])
    with pytest.raises(ValueError):
        message_unpin(reg_dict1['token'], message_dict1['message_id'])

def test_message_unpin_not_admin():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], create_dict1['channel_id'])
    channel_join(reg_dict3['token'], create_dict1['channel_id'])

    message_dict1 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Message 0")
    message_dict2 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Oof")
    message_dict3 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Ouch")
    message_dict4 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Owie")

    create_dict2 = channels_create(reg_dict2['token'], 'PCSoc', True)
    channel_join(reg_dict2['token'], create_dict2['channel_id'])
    # SETUP END

    message_pin(reg_dict1['token'], message_dict1['message_id'])
    # Can't unpin if the user is not an admin for the message's channel
    with pytest.raises(ValueError):
        message_unpin(reg_dict2['token'], message_dict1['message_id'])
    assert message_unpin(reg_dict1['token'], message_dict1['message_id']) == {}

    message_pin(reg_dict1['token'], message_dict4['message_id'])
    with pytest.raises(ValueError):
        message_unpin(reg_dict2['token'], message_dict4['message_id'])
    assert message_unpin(reg_dict1['token'], message_dict4['message_id']) == {}

    # Adding users as owners/admins should allow them to unpin
    message_pin(reg_dict1['token'], message_dict2['message_id'])
    with pytest.raises(ValueError):
        message_unpin(reg_dict2['token'], message_dict2['message_id'])
    channel_addowner(reg_dict1['token'], create_dict1['channel_id'], reg_dict2['u_id'])
    assert message_unpin(reg_dict2['token'], message_dict2['message_id']) == {}

    # After losing ownership their unpinned messages stay unpinned
    channel_removeowner(reg_dict1['token'], create_dict1['channel_id'], reg_dict2['u_id'])
    with pytest.raises(ValueError):
        message_unpin(reg_dict1['token'], message_dict2['message_id'])

    # But they also can't unpin anymore messages
    message_pin(reg_dict1['token'], message_dict3['message_id'])
    with pytest.raises(ValueError):
        message_unpin(reg_dict2['token'], message_dict3['message_id'])

def test_message_unpin_already_unpinned():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict2['token'], 'PCSoc', False)

    channel_invite(reg_dict2['token'], create_dict1['channel_id'], reg_dict1['u_id'])

    message_dict1 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Oof")
    message_dict2 = message_send(reg_dict2['token'], create_dict1['channel_id'], "Ouch")

    message_pin(reg_dict1['token'], message_dict1['message_id'])
    message_pin(reg_dict2['token'], message_dict2['message_id'])
    # SETUP END

    assert message_unpin(reg_dict1['token'], message_dict1['message_id']) == {}
    assert message_unpin(reg_dict2['token'], message_dict2['message_id']) == {}

    with pytest.raises(ValueError):
        message_unpin(reg_dict1['token'], message_dict1['message_id'])
    with pytest.raises(ValueError):
        message_unpin(reg_dict2['token'], message_dict2['message_id'])
    with pytest.raises(ValueError):
        message_unpin(reg_dict2['token'], message_dict1['message_id'])
    with pytest.raises(ValueError):
        message_unpin(reg_dict1['token'], message_dict2['message_id'])

    # Unpinned message are repinnable
    assert message_pin(reg_dict1['token'], message_dict1['message_id']) == {}
    assert message_pin(reg_dict2['token'], message_dict2['message_id']) == {}

def test_message_unpin_not_in_channel():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')

    create_dict1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    create_dict2 = channels_create(reg_dict2['token'], 'PCSoc', False)

    message_dict1 = message_send(reg_dict1['token'], create_dict1['channel_id'], "Oof")
    message_dict2 = message_send(reg_dict2['token'], create_dict2['channel_id'], "Ouch")

    message_pin(reg_dict1['token'], message_dict1['message_id'])
    message_pin(reg_dict2['token'], message_dict2['message_id'])
    # SETUP END

    with pytest.raises(AccessError):
        message_unpin(reg_dict1['token'], message_dict2['message_id'])
    with pytest.raises(AccessError):
        message_unpin(reg_dict2['token'], message_dict1['message_id'])
    