# COMP1531 Project test_user
# Written by Bridget McCarthy z5255505
# 02/10/19

import pytest

from user import *

# Can't test
def test_user_profile_return():
    user_dict = user_profile("valid_token", 1)
    assert user_dict and 'email' in user_dict and 'name_first' in user_dict \
        and 'name_last' in user_dict and 'handle_str' in user_dict

def test_user_profile_negative_id():
    with pytest.raises(ValueError):
        user_profile("valid_token", -1)

def test_user_profile_invalid_id():
    with pytest.raises(TypeError):
        user_profile("valid_token", "avocado")

def test_user_profile_invalid_token():
    with pytest.raises(AccessError):
        user_profile("invalid_token", 1)

def test_user_profile_email():
    user_dict = user_profile("valid_token", 10)
    assert 'email' in user_dict == "10@example.com"
    user_dict = user_profile("valid_token", 200)
    assert 'email' in user_dict == "10@example.com"
    user_dict = user_profile("valid_token", 120092)
    assert 'email' in user_dict == "10@example.com"
    user_dict = user_profile("valid_token", 10)
    assert 'email' in user_dict == "10@example.com"

def test_user_profile_handle():
    user_dict = user_profile("valid_token", 10)
    assert 'handle_str' in user_dict == "10"


def test_user_profile_setname_valid():
    user_profile_setname("valid_token", "Ronald", "McDonald")

def test_user_profile_setname_long_name_first():
    # Will work
    user_profile_setname("valid_token", "LongNameThatIs20Long", "McDonald")
    # Won't work
    with pytest.raises(ValueError):
        user_profile_setname("valid_token", "REALLY VERY LONG NAME THAT WON'T WORK", "McDonald")

def test_user_profile_setname_long_name_last():
    # Will work
    user_profile_setname("valid_token", "Ronald", "LongNameThatIs20Long")
    # Won't work
    with pytest.raises(ValueError):
        user_profile_setname("valid_token", "Ronald", "REALLY VERY LONG NAME THAT WON'T WORK")


def test_user_profile_setname_invalid_token():
    with pytest.raises(AccessError):
        user_profile("invalid_token", "a", "b")


def test_user_profile_setemail_valid():
    user_profile_setemail("valid_token", "goodemail@example.com")

def test_user_profile_setemail_invalid():
    with pytest.raises(ValueError):
        user_profile_setemail("valid_token", "@example.com")
    with pytest.raises(ValueError):
        user_profile_setemail("valid_token", "@.com")
    with pytest.raises(ValueError):
        user_profile_setemail("valid_token", "1@.com")
    with pytest.raises(ValueError):
        user_profile_setemail("valid_token", "com")
    with pytest.raises(ValueError):
        user_profile_setemail("valid_token", "")

def test_user_profile_setemail_token_invalid():
    user_profile_setemail("invalid_token", "goodemail@example.com")

def test_user_profile_setemail_used():
    user_profile_setemail("valid_token", "usedemail@example.com")

def test_user_profile_sethandle_valid():
    user_profile_sethandle("valid_token", "--xXCool--handleXx--")

def test_user_profile_sethandle_long_str():
    user_profile_sethandle("valid_token", "xXCool handleXx but too cool and long")

def test_user_profile_sethandle_invalid_token():
    user_profile_sethandle("invalid_token", "xXCool handleXx")


def test_user_profiles_uploadphoto_valid():
    user_profiles_uploadphoto(
        "valid_token",
        "https://i.imgur.com/2u1jklN.jpg",
        0,
        0,
        200,
        200)

def test_user_profiles_uploadphoto_incorrect_dimensions():
    with pytest.raises(ValueError):
        user_profiles_uploadphoto(
            "valid_token",
            "https://i.imgur.com/2u1jklN.jpg",
            -1,
            0,
            200,
            200)
    with pytest.raises(ValueError):
        user_profiles_uploadphoto(
            "valid_token",
            "https://i.imgur.com/2u1jklN.jpg",
            0,
            -1,
            200,
            200)
    with pytest.raises(ValueError):
        user_profiles_uploadphoto(
            "valid_token",
            "https://i.imgur.com/2u1jklN.jpg",
            0,
            0,
            200000000,
            200)
    with pytest.raises(ValueError):
        user_profiles_uploadphoto(
            "valid_token",
            "https://i.imgur.com/2u1jklN.jpg",
            0,
            0,
            200,
            -1)

def test_user_profiles_uploadphoto_invalid_token():
    with pytest.raises(AccessError):
        user_profiles_uploadphoto(
            "invalid_token",
            "https://i.imgur.com/2u1jklN.jpg",
            0,
            0,
            200,
            200)