# COMP1531 Project test_users
# Written by Sabine Lim z5242579
# 12/11/19

from .auth import auth_register
from .users import users_all
from .user import (
    user_profile_setname, user_profile_setemail, user_profile_sethandle,
    user_profiles_uploadphoto
)
from .db import reset_data

def test_users_all_simple():
    # SETUP BEGIN
    reset_data()
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    # SETUP END

    users = users_all(reg_dict1['token'])

    assert users[0] == {
        'u_id': reg_dict1['u_id'],
        'email': 'user@example.com',
        'name_first': 'Test',
        'name_last': 'User',
        'handle_str': 'TestUser',
        'profile_img_url': None
    }

    assert users[1] == {
        'u_id': reg_dict2['u_id'],
        'email': 'sabine.lim@unsw.edu.au',
        'name_first': 'Sabine',
        'name_last': 'Lim',
        'handle_str': 'SabineLim',
        'profile_img_url': None
    }

    assert users[2] == {
        'u_id': reg_dict3['u_id'],
        'email': 'gamer@twitch.tv',
        'name_first': 'Gabe',
        'name_last': 'Newell',
        'handle_str': 'GabeNewell',
        'profile_img_url': None
    }

def test_users_all_one():
    # SETUP BEGIN
    reset_data()
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    # SETUP END

    assert users_all(reg_dict1['token'])[0] == {
        'u_id': reg_dict1['u_id'],
        'email': 'user@example.com',
        'name_first': 'Test',
        'name_last': 'User',
        'handle_str': 'TestUser',
        'profile_img_url': None
    }

def test_users_all_update_profile():
    # SETUP BEGIN
    reset_data()
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    # SETUP END

    assert users_all(reg_dict1['token'])[0] == {
        'u_id': reg_dict1['u_id'],
        'email': 'user@example.com',
        'name_first': 'Test',
        'name_last': 'User',
        'handle_str': 'TestUser',
        'profile_img_url': None
    }

    user_profile_setname(reg_dict1['token'], 'Test2', 'ElectricBoogaloo')
    user_profile_setemail(reg_dict1['token'], 'john.appleseed@example.com')
    user_profile_sethandle(reg_dict1['token'], 'Testificate')
    user_profiles_uploadphoto(reg_dict1['token'], 'https://i.imgur.com/43wtR5u.jpg', 0, 0, 638, 905)
    
    assert users_all(reg_dict1['token'])[0] == {
        'u_id': reg_dict1['u_id'],
        'email': 'john.appleseed@example.com',
        'name_first': 'Test2',
        'name_last': 'ElectricBoogaloo',
        'handle_str': 'Testificate',
        'profile_img_url': 'https://i.imgur.com/43wtR5u.jpg'
    }

def test_users_all_not_slackr_owner():
    # SETUP BEGIN
    reset_data()
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    # SETUP END

    users = users_all(reg_dict3['token'])

    assert users[0] == {
        'u_id': reg_dict1['u_id'],
        'email': 'user@example.com',
        'name_first': 'Test',
        'name_last': 'User',
        'handle_str': 'TestUser',
        'profile_img_url': None
    }

    assert users[1] == {
        'u_id': reg_dict2['u_id'],
        'email': 'sabine.lim@unsw.edu.au',
        'name_first': 'Sabine',
        'name_last': 'Lim',
        'handle_str': 'SabineLim',
        'profile_img_url': None
    }

    assert users[2] == {
        'u_id': reg_dict3['u_id'],
        'email': 'gamer@twitch.tv',
        'name_first': 'Gabe',
        'name_last': 'Newell',
        'handle_str': 'GabeNewell',
        'profile_img_url': None
    }
