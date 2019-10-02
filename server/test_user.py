# COMP1531 Project test_user
# Written by Bridget McCarthy z5255505
# 02/10/19

import pytest

from auth import *
from user import *

# Can't test
def test_user_profile_return():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    # SETUP END
    user_dict = user_profile(reg_dict1['token'], 1234567)
    assert user_dict and user_dict['email'] and user_dict['name_first'] \
        and user_dict['name_last'] and user_dict['handle_str']

def test_user_profile_negative_id():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    # SETUP END
    with pytest.raises(ValueError):
        user_profile(reg_dict1['token'], -1)

def test_user_profile_invalid_id():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    # SETUP END
    with pytest.raises(TypeError):
        user_profile(reg_dict1['token'], "avocado")

def test_user_profile_data():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    # SETUP END
    user_dict = user_profile(reg_dict1['token'], 1234567)
    assert user_dict['email'] == "user@example.com"
    assert user_dict['name_first'] == "Test"
    assert user_dict['name_last'] == "User"
    assert user_dict['handle_str'] == "TestUser"
    user_dict = user_profile(reg_dict2['token'], 5242579)
    assert user_dict['email'] == "sabine.lim@unsw.edu.au"
    assert user_dict['name_first'] == "Sabine"
    assert user_dict['name_last'] == "Lim"
    assert user_dict['handle_str'] == "SabineLim"
    user_dict = user_profile(reg_dict3['token'], 4201337)
    assert user_dict['email'] == "gamer@twitch.tv"
    assert user_dict['name_first'] == "Gabe"
    assert user_dict['name_last'] == "Newell"
    assert user_dict['handle_str'] == "GabeNewell"

def test_user_profile_handle():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    # SETUP END
    user_dict1 = user_profile(reg_dict1['token'], 1234567)
    user_dict2 = user_profile(reg_dict2['token'], 5242579)
    user_dict3 = user_profile(reg_dict3['token'], 4201337)
    assert user_dict1['handle_str'] == "1234567"
    assert user_dict2['handle_str'] == "5242579"
    assert user_dict3['handle_str'] == "4201337"

def test_user_profile_setname_valid():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    # SETUP END
    user_profile_setname(reg_dict1['token'], "Ronald", "McDonald")
    user_dict1 = user_profile(reg_dict1['token'], 1234567)
    assert user_dict1['name_first'] == "Ronald" and user_dict1['name_last'] == "McDonald"

    user_profile_setname(reg_dict2['token'], "Donald", "McDonald")
    user_dict2 = user_profile(reg_dict2['token'], 5242579)
    assert user_dict2['name_first'] == "Donald" and user_dict2['name_last'] == "McDonald"
    
    user_profile_setname(reg_dict3['token'], "Tonald", "McDonald")
    user_dict3 = user_profile(reg_dict3['token'], 4201337)
    assert user_dict3['name_first'] == "Tonald" and user_dict3['name_last'] == "McDonald"

def test_user_profile_setname_long_name_first():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    # SETUP END
    # Will work
    user_profile_setname(reg_dict1['token'], "LongNameThatIs20Long", "McDonald")
    # Won't work
    with pytest.raises(ValueError):
        user_profile_setname(reg_dict1['token'], "REALLY VERY LONG NAME THAT WON'T WORK", "McDonald")

def test_user_profile_setname_long_name_last():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    # SETUP END
    # Will work
    user_profile_setname(reg_dict1['token'], "Ronald", "LongNameThatIs20Long")
    # Won't work
    with pytest.raises(ValueError):
        user_profile_setname(reg_dict1['token'], "Ronald", "REALLY VERY LONG NAME THAT WON'T WORK")


def test_user_profile_setemail_valid():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    # SETUP END
    user_profile_setemail(reg_dict1['token'], "goodemail@example.com")
    user_dict = user_profile(reg_dict1['token'], 1234567)
    assert user_dict['email'] == "goodemail@example.com"

    user_profile_setemail(reg_dict1['token'], "user@example.com")
    user_dict = user_profile(reg_dict1['token'], 1234567)
    assert user_dict['email'] == "user@example.com"

    user_profile_setemail(reg_dict1['token'], "user@example.com")
    user_dict = user_profile(reg_dict1['token'], 1234567)
    assert user_dict['email'] == "user@example.com"

    user_profile_setemail(reg_dict1['token'], "goodemail23@example.com")
    user_dict = user_profile(reg_dict1['token'], 1234567)
    assert user_dict['email'] == "goodemail23@example.com"

    user_profile_setemail(reg_dict1['token'], "goodemail@msn.com")
    user_dict = user_profile(reg_dict1['token'], 1234567)
    assert user_dict['email'] == "goodemail@msn.com"

def test_user_profile_setemail_invalid():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    # SETUP END
    with pytest.raises(ValueError):
        user_profile_setemail(reg_dict1['token'], "@example.com")
    with pytest.raises(ValueError):
        user_profile_setemail(reg_dict1['token'], "@.com")
    with pytest.raises(ValueError):
        user_profile_setemail(reg_dict1['token'], "1@.com")
    with pytest.raises(ValueError):
        user_profile_setemail(reg_dict1['token'], "com")
    with pytest.raises(ValueError):
        user_profile_setemail(reg_dict1['token'], "")

def test_user_profile_setemail_used():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    # SETUP END
    with pytest.raises(ValueError):
        user_profile_setemail(reg_dict1['token'], "sabine.lim@unsw.edu.au")

def test_user_profile_sethandle_valid():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    # SETUP END
    user_profile_sethandle(reg_dict1['token'], "--xXCool--handleXx--")
    user_dict = user_profile(reg_dict1['token'], 1234567)
    assert user_dict['handle_str'] == "--xXCool--handleXx--"

    user_profile_sethandle(reg_dict1['token'], "aaa")
    user_dict = user_profile(reg_dict1['token'], 1234567)
    assert user_dict['handle_str'] == "aaa"

def test_user_profile_sethandle_long_str():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    # SETUP END
    with pytest.raises(ValueError):
        user_profile_sethandle(reg_dict1['token'], "xXCool handleXx but too cool and long")

def test_user_profiles_uploadphoto_valid():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    # SETUP END
    user_profiles_uploadphoto(
        reg_dict1['token'],
        "https://i.imgur.com/2u1jklN.jpg",
        0,
        0,
        200,
        200)
    user_profiles_uploadphoto(
        reg_dict1['token'],
        "https://i.imgur.com/2u1jklN.jpg",
        0,
        0,
        100,
        100)

def test_user_profiles_uploadphoto_http_error():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    # SETUP END
    with pytest.raises(ValueError):
        user_profiles_uploadphoto(
            reg_dict1['token'],
            "https",
            0,
            0,
            200,
            200)
    with pytest.raises(ValueError):
        user_profiles_uploadphoto(
            reg_dict1['token'],
            "a.jpg",
            0,
            0,
            200,
            200)
    with pytest.raises(ValueError):
        user_profiles_uploadphoto(
            reg_dict1['token'],
            "https://www.google.com/",
            0,
            0,
            200,
            200)

def test_user_profiles_uploadphoto_incorrect_dimensions():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    # SETUP END
    with pytest.raises(ValueError):
        user_profiles_uploadphoto(
            reg_dict1['token'],
            "https://i.imgur.com/2u1jklN.jpg",
            -1,
            0,
            200,
            200)
    with pytest.raises(ValueError):
        user_profiles_uploadphoto(
            reg_dict1['token'],
            "https://i.imgur.com/2u1jklN.jpg",
            0,
            -1,
            200,
            200)
    with pytest.raises(ValueError):
        user_profiles_uploadphoto(
            reg_dict1['token'],
            "https://i.imgur.com/2u1jklN.jpg",
            0,
            0,
            200000000,
            200)
    with pytest.raises(ValueError):
        user_profiles_uploadphoto(
            reg_dict1['token'],
            "https://i.imgur.com/2u1jklN.jpg",
            0,
            0,
            200,
            -1)
