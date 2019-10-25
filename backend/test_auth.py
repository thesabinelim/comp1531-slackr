# COMP1531 Project auth tests
# Written by Sabine Lim z5242579
# 29/09/19

import pytest

from .db import reset_data
from .auth import (
    auth_register, auth_login, auth_logout, auth_passwordreset_request,
    auth_passwordreset_reset
)
from .user import user_profile
from .error import ValueError, InvalidTokenError

#######################
# auth_register Tests #
#######################

def test_auth_register_simple():
    # SETUP BEGIN
    reset_data()
    # SETUP END

    # Register new user Test
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    assert 'u_id' in reg_dict1 and 'token' in reg_dict1

    # Register new user Sabine
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    assert 'u_id' in reg_dict2 and 'token' in reg_dict2

    # Check that registration attempts returned different values
    assert reg_dict2['u_id'] != reg_dict1['u_id']
    assert reg_dict2['token'] != reg_dict1['token']

    # Register new user Gabe
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    assert reg_dict3 and 'u_id' in reg_dict3 and 'token' in reg_dict3

    # Check that registration attempts returned different values
    assert reg_dict1['u_id'] != reg_dict2['u_id'] != reg_dict3['u_id']
    assert reg_dict1['token'] != reg_dict2['token'] != reg_dict3['token']

    # Check that authorisation attempts succeed
    user_profile(reg_dict1['token'], reg_dict1['u_id'])
    user_profile(reg_dict2['token'], reg_dict2['u_id'])
    user_profile(reg_dict3['token'], reg_dict3['u_id'])

def test_auth_register_handle_concat_simple():
    # SETUP BEGIN
    reset_data()
    # SETUP END

    # Register new user Test
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    assert 'u_id' in reg_dict1 and 'token' in reg_dict1
    profile_dict1 = user_profile(reg_dict1['token'], reg_dict1['u_id'])

    assert profile_dict1['handle_str'] == "testuser"

def test_auth_register_handle_too_long():
    # SETUP BEGIN
    reset_data()
    # SETUP END

    # Register new user Whatsup
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Whatsup', 'Mynameistoolong')
    assert 'u_id' in reg_dict1 and 'token' in reg_dict1
    profile_dict1 = user_profile(reg_dict1['token'], reg_dict1['u_id'])

    # Check that handle is cut off after 20 characters
    assert profile_dict1['handle_str'] == "whatsupmynameistoolo"

def test_auth_register_unique_handle():
    # SETUP BEGIN
    reset_data()
    # SETUP END

    # Register new user Test
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    assert 'u_id' in reg_dict1 and 'token' in reg_dict1
    profile_dict1 = user_profile(reg_dict1['token'], reg_dict1['u_id'])

    # Register another user with same names as Test
    reg_dict2 = auth_register('user2@example.com', 'validpassword', 'Test', 'User')
    assert 'u_id' in reg_dict2 and 'token' in reg_dict2
    profile_dict2 = user_profile(reg_dict2['token'], reg_dict2['u_id'])

    # Register yet another user with same names as Test
    reg_dict3 = auth_register('user3@example.com', 'validpassword', 'Test', 'User')
    assert 'u_id' in reg_dict3 and 'token' in reg_dict3
    profile_dict3 = user_profile(reg_dict3['token'], reg_dict3['u_id'])

    # Check that user handles are different despite user's names being identical
    assert profile_dict1['handle_str'] != profile_dict2['handle_str'] \
        != profile_dict3['handle_str']

def test_auth_register_invalid_email():
    # SETUP BEGIN
    reset_data()
    # SETUP END

    with pytest.raises(ValueError):
        auth_register('bademail', 'validpassword', 'Test', 'User')

def test_auth_register_invalid_password():
    # SETUP BEGIN
    reset_data()
    # SETUP END

    with pytest.raises(ValueError):
        auth_register('user@example.com', 'pwd', 'Test', 'User')

def test_auth_register_invalid_names():
    # SETUP BEGIN
    reset_data()
    # SETUP END

    with pytest.raises(ValueError):
        auth_register('user@example.com', 'validpassword', \
        '123456789012345678901234567890123456789012345678901', 'User')
    with pytest.raises(ValueError):
        auth_register('user@example.com', 'validpassword', 'Test', \
        '123456789012345678901234567890123456789012345678901')

def test_auth_register_email_taken():
    # SETUP BEGIN
    reset_data()

    auth_register('user@example.com', 'validpassword', 'Test', 'User')
    auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    # SETUP END

    with pytest.raises(ValueError):
        auth_register('user@example.com', 'validpassword', 'Test', 'User')
    with pytest.raises(ValueError):
        auth_register('user@example.com', 'diffpassword', 'Test', 'User')

    with pytest.raises(ValueError):
        auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    with pytest.raises(ValueError):
        auth_register('sabine.lim@unsw.edu.au', 'diffpassword', 'Sabine', 'Lim')

    with pytest.raises(ValueError):
        auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    with pytest.raises(ValueError):
        auth_register('gamer@twitch.tv', 'diffpassword', 'Gabe', 'Newell')

####################
# auth_login Tests #
####################

def test_auth_login_simple():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    # SETUP END

    # Login as Test
    login_dict1 = auth_login('user@example.com', 'validpassword')
    assert 'u_id' in login_dict1 and 'token' in login_dict1
    assert login_dict1['u_id'] == reg_dict1['u_id']

    # Login as Sabine
    login_dict2 = auth_login('sabine.lim@unsw.edu.au', 'ImSoAwes0me')
    assert 'u_id' in login_dict2 and 'token' in login_dict2
    assert login_dict2['u_id'] == reg_dict2['u_id']

    # Login as Gabe
    login_dict3 = auth_login('gamer@twitch.tv', 'gamers_rise_up')
    assert 'u_id' in login_dict3 and 'token' in login_dict3
    assert login_dict3['u_id'] == reg_dict3['u_id']

    # Check that authorisation attempts succeed
    user_profile(login_dict1['token'], login_dict1['u_id'])
    user_profile(login_dict2['token'], login_dict2['u_id'])
    user_profile(login_dict3['token'], login_dict3['u_id'])

def test_auth_login_invalid_email():
    # SETUP BEGIN
    reset_data()
    # SETUP END

    with pytest.raises(ValueError):
        auth_login('bademail', 'pwd')

def test_auth_login_email_not_registered():
    # SETUP BEGIN
    reset_data()
    # SETUP END

    with pytest.raises(ValueError):
        auth_login('idontexist@example.com', 'validpassword')

def test_auth_login_wrong_password():
    # SETUP BEGIN
    reset_data()

    auth_register('user@example.com', 'validpassword', 'Test', 'User')
    auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    # SETUP END

    with pytest.raises(ValueError):
        auth_login('user@example.com', 'wrongpassword')
    with pytest.raises(ValueError):
        auth_login('sabine.lim@unsw.edu.au', 'wrongpassword')
    with pytest.raises(ValueError):
        auth_login('gamer@twitch.tv', 'wrongpassword')

#####################
# auth_logout Tests #
#####################

def test_auth_logout_simple():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    # SETUP END

    assert auth_logout(reg_dict1['token']) == {'is_success': True}
    assert auth_logout(reg_dict2['token']) == {'is_success': True}
    assert auth_logout(reg_dict3['token']) == {'is_success': True}

    # Check that future authorisation attempts fail
    with pytest.raises(InvalidTokenError):
        user_profile(reg_dict1['token'], reg_dict1['u_id'])
    with pytest.raises(InvalidTokenError):
        user_profile(reg_dict2['token'], reg_dict2['u_id'])
    with pytest.raises(InvalidTokenError):
        user_profile(reg_dict3['token'], reg_dict3['u_id'])

def test_auth_logout_invalidated_token():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    # SETUP END

    assert auth_logout(reg_dict1['token']) == {'is_success': True}
    assert auth_logout(reg_dict1['token']) == {'is_success': False}

####################################
# auth_passwordreset_request Tests #
####################################

def test_passwordreset_request_simple():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    # SETUP END

    assert auth_passwordreset_request('user@example.com') == {}
    assert auth_passwordreset_request('sabine.lim@unsw.edu.au') == {}
    assert auth_passwordreset_request('gamer@twitch.tv') == {}

##################################
# auth_passwordreset_reset Tests #
##################################

# These tests will need to be reworked once auth_passwordreset_request is
# actually implemented, as right now they're using hard coded reset tokens

def test_passwordreset_reset_simple():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    # SETUP END

    assert auth_passwordreset_reset('abcdef', 'alsovalidpwd') == {}
    assert auth_passwordreset_reset('cfa027', 'kindaAwesomeIGuess') == {}
    assert auth_passwordreset_reset('bb809m', 'or_sitThat5fineT00') == {}

def test_passwordreset_reset_badpwd():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    # SETUP END

    with pytest.raises(ValueError):
        auth_passwordreset_reset('abcdef', 'pwd')
    with pytest.raises(ValueError):
        auth_passwordreset_reset('cfa027', 'pwd')
    with pytest.raises(ValueError):
        auth_passwordreset_reset('bb809m', 'pwd')
