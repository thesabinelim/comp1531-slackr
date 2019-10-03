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
    # !!!!!!!!!! TODO
    
def test_message_react_simple():
    pass

def test_message_react_message_invalid():
    pass

def test_message_react_react_invalid():
    pass

def test_message_react_message_already_reacted():
    pass
    
def test_message_unreact():
    pass
    
def test_message_pin():
    pass
    
def test_message_unpin():
    pass
    