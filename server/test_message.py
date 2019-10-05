# test_message.py
# Authored by Bridget McCarthy 29/09/19

import datetime
import pytest

from auth import *
from message import *
from channel import *
from channels import *

def test_message_sendlater_simple():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    channel_1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], channel_1['channel_id'])
    channel_join(reg_dict3['token'], channel_1['channel_id'])
    now = datetime.datetime.now()
    # SETUP END
    now_plus_mins = now + datetime.timedelta(minutes = 10)
    message_sendlater(reg_dict1['token'], channel_1['channel_id'], "Oof", now_plus_mins)
    
    now_plus_hour = now + datetime.timedelta(hours = 1)
    message_sendlater(reg_dict2['token'], channel_1['channel_id'], "Ouch", now_plus_hour)

    now_plus_days = now + datetime.timedelta(days = 3)
    message_sendlater(reg_dict3['token'], channel_1['channel_id'], "Owie", now_plus_days)

def test_message_sendlater_long_message():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')  
    channel_1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    now = datetime.datetime.now()
    # SETUP END
    now_plus_mins = now + datetime.timedelta(minutes = 10)
    too_long_msg = "If you take the temperature of a superconductor down to absolute zero (around minus 273.1 centigrade), it ignores gravity and floats. This is a scientific fact and you are welcome to check - google or youtube it. My 9yo son asked why we couldn't freeze a car to -273C and fly in it and I told him that the car would neutralise gravity, not reverse it and the weight of the people in it would make it sink. Also, heat rises so -273C should really sink unless it was in a vacuum which means we wouldn't be able to breath or hear the stereo. You would also need to rug up well. If you take the temperature of a superconductor down to absolute zero (around minus 273.1 centigrade), it ignores gravity and floats. This is a scientific fact and you are welcome to check - google or youtube it. My 9yo son asked why we couldn't freeze a car to -273C and fly in it and I told him that the car would neutralise gravity, not reverse it and the weight of the people in it would make it sink. Also, heat rises so -273C should really sink unless it was in a vacuum which means we wouldn't be able to breath or hear the stereo. You would also need to rug up well."
    with pytest.raises(ValueError):
        message_sendlater(reg_dict1['token'], channel_1['channel_id'], too_long_msg, now_plus_mins)
    
def test_message_sendlater_invalid_channel():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')  
    channel_1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    now = datetime.datetime.now()
    # SETUP END
    now_plus_mins = now + datetime.timedelta(minutes = 10)
    with pytest.raises(ValueError):
        message_sendlater(reg_dict1['token'], -1000, "Oof", now_plus_mins)

def test_message_sendlater_past_time():
     # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')  
    channel_1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    now = datetime.datetime.now()
    # SETUP END
    now_minus_mins = now - datetime.timedelta(minutes = 10)
    with pytest.raises(ValueError):
        message_sendlater(reg_dict1['token'], channel_1['channel_id'], "Oof", now_minus_mins)
    
def test_message_send_simple():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    channel_1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], channel_1['channel_id'])
    channel_join(reg_dict3['token'], channel_1['channel_id'])
    # SETUP END
    message_send(reg_dict1['token'], channel_1['channel_id'], "Oof")
    message_send(reg_dict2['token'], channel_1['channel_id'], "Ouch")
    message_send(reg_dict3['token'], channel_1['channel_id'], "Owie")

def test_message_send_too_long_message():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    channel_1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END
    too_long_msg = "If you take the temperature of a superconductor down to absolute zero (around minus 273.1 centigrade), it ignores gravity and floats. This is a scientific fact and you are welcome to check - google or youtube it. My 9yo son asked why we couldn't freeze a car to -273C and fly in it and I told him that the car would neutralise gravity, not reverse it and the weight of the people in it would make it sink. Also, heat rises so -273C should really sink unless it was in a vacuum which means we wouldn't be able to breath or hear the stereo. You would also need to rug up well. If you take the temperature of a superconductor down to absolute zero (around minus 273.1 centigrade), it ignores gravity and floats. This is a scientific fact and you are welcome to check - google or youtube it. My 9yo son asked why we couldn't freeze a car to -273C and fly in it and I told him that the car would neutralise gravity, not reverse it and the weight of the people in it would make it sink. Also, heat rises so -273C should really sink unless it was in a vacuum which means we wouldn't be able to breath or hear the stereo. You would also need to rug up well."
    with pytest.raises(ValueError):
        message_send(reg_dict1['token'], too_long_msg, "Oof")
    
def test_message_remove_simple():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    channel_1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END
    message_send(reg_dict1['token'], channel_1['channel_id'], "Oof")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Ouch")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Owie")
    message_remove(reg_dict1['token'], 1)
    message_remove(reg_dict1['token'], 2)
    message_remove(reg_dict1['token'], 3)

def test_message_remove_removed_message():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    channel_1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    # SETUP END
    message_send(reg_dict1['token'], channel_1['channel_id'], "Oof")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Ouch")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Owie")
    message_remove(reg_dict1['token'], 1)
    message_remove(reg_dict1['token'], 2)
    message_remove(reg_dict1['token'], 3)
    with pytest.raises(ValueError):
        message_remove(reg_dict1['token'], 1)
    with pytest.raises(ValueError):
        message_remove(reg_dict1['token'], 2)
    with pytest.raises(ValueError):
        message_remove(reg_dict1['token'], 3)

def test_message_remove_message_access_error():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    
    channel_1 = channels_create(reg_dict1['token'], '1531 autotest', True)
    channel_join(reg_dict2['token'], channel_1['channel_id'])
    channel_join(reg_dict3['token'], channel_1['channel_id'])
    # SETUP END
    message_send(reg_dict1['token'], channel_1['channel_id'], "Oof")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Ouch")
    message_send(reg_dict1['token'], channel_1['channel_id'], "Owie")
    # Message sent by user
    message_remove(reg_dict1['token'], 2)
    # Message sent by owner of the channel, but not by the user
    with pytest.raises(AccessError):
        message_remove(reg_dict2['token'], 1)
    with pytest.raises(AccessError):
        message_remove(reg_dict2['token'], 3)

    # Message was sent by random
    message_send(reg_dict2['token'], channel_1['channel_id'], "Oof")
    message_send(reg_dict2['token'], channel_1['channel_id'], "Ouch")
    message_send(reg_dict2['token'], channel_1['channel_id'], "Owie")
    # TODO !!!!!!!!!!!!!!!!!!!!
    
    
    
def test_message_edit():
    pass
    # !!!!!!!!!! TODO
    
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

    
def test_message_pin_simple():
    pass

def test_message_pin_invalid_message():
    pass

def test_message_pin_user_not_admin():
    pass

def test_message_pin_already_pinned():
    pass

def test_message_unpin_simple():
    pass

def test_message_unpin_invalid_message():
    pass

def test_message_unpin_user_not_admin():
    pass

def test_message_unpin_already_pinned():
    pass
    