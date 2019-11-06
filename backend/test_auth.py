# COMP1531 Project auth tests
# Written by Sabine Lim z5242579
# 29/09/19

import pytest
import re
import time
import jwt

from .db import reset_data
from .auth import (
    auth_register, auth_login, auth_logout, auth_passwordreset_request,
    auth_passwordreset_reset
)
from .user import user_profile
from .utils import random_string
from .error import ValueError, AccessError

###########################
# Counterfeit Token Tests #
###########################

# Return a new token given u_id.
def generate_counterfeit_token(u_id):
    counterfeit_secret = 'counterfeit'
    token_bytes = jwt.encode(
        {
            'u_id': u_id,
            'timestamp': time.time()
        }, counterfeit_secret, algorithm='HS256'
    )
    token = token_bytes.decode('utf-8')
    return token

def test_counterfeit_token():
    # SETUP BEGIN
    reset_data()

    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    # SETUP END

    counterfeit_token1 = generate_counterfeit_token(reg_dict1['u_id'])
    with pytest.raises(AccessError):
        user_profile(counterfeit_token1, reg_dict1['u_id'])

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
    with pytest.raises(AccessError):
        user_profile(reg_dict1['token'], reg_dict1['u_id'])
    with pytest.raises(AccessError):
        user_profile(reg_dict2['token'], reg_dict2['u_id'])
    with pytest.raises(AccessError):
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

reset_email_title = 'Your password reset code'
reset_email_body_re = re.compile(r'Your reset code is [a-z0-9]{6} and will expire in 5 minutes.')

def test_passwordreset_request_simple():
    # SETUP BEGIN
    reset_data()

    auth_register('user@example.com', 'validpassword', 'Test', 'User')
    auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    # SETUP END

    request_dict1 = auth_passwordreset_request('user@example.com')
    assert request_dict1['recipients'] == ['user@example.com']
    assert request_dict1['title'] == reset_email_title
    assert reset_email_body_re.fullmatch(request_dict1['body']) is not None

    request_dict2 = auth_passwordreset_request('sabine.lim@unsw.edu.au')
    assert request_dict2['recipients'] == ['sabine.lim@unsw.edu.au']
    assert request_dict2['title'] == reset_email_title
    assert reset_email_body_re.fullmatch(request_dict2['body']) is not None

    request_dict3 = auth_passwordreset_request('gamer@twitch.tv')
    assert request_dict3['recipients'] == ['gamer@twitch.tv']
    assert request_dict3['title'] == reset_email_title
    assert reset_email_body_re.fullmatch(request_dict3['body']) is not None

def test_passwordreset_request_no_match():
    # SETUP BEGIN
    reset_data()
    # SETUP END

    assert auth_passwordreset_request('user@example.com') == {}

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

    request_dict1 = auth_passwordreset_request('user@example.com')
    reset_code1 = request_dict1['body'][19:25]

    request_dict2 = auth_passwordreset_request('sabine.lim@unsw.edu.au')
    reset_code2 = request_dict2['body'][19:25]

    request_dict3 = auth_passwordreset_request('gamer@twitch.tv')
    reset_code3 = request_dict3['body'][19:25]
    # SETUP END

    # Reset passwords
    assert auth_passwordreset_reset(reset_code1, 'alsovalidpwd') == {}
    assert auth_passwordreset_reset(reset_code2, 'kindaAwesomeIGuess') == {}
    assert auth_passwordreset_reset(reset_code3, 'or_sitThat5fineT00') == {}

    # Check that old passwords are no longer valid
    with pytest.raises(ValueError):
        auth_login('user@example.com', 'validpassword')
    with pytest.raises(ValueError):
        auth_login('sabine.lim@unsw.edu.au', 'ImSoAwes0me')
    with pytest.raises(ValueError):
        auth_login('gamer@twitch.tv', 'gamers_rise_up')

    # Attempt login with new passwords
    auth_login('user@example.com', 'alsovalidpwd')
    auth_login('sabine.lim@unsw.edu.au', 'kindaAwesomeIGuess')
    auth_login('gamer@twitch.tv', 'or_sitThat5fineT00')

def test_passwordreset_reset_invalid_code():
    # SETUP BEGIN
    reset_data()

    auth_register('user@example.com', 'validpassword', 'Test', 'User')

    request_dict1 = auth_passwordreset_request('user@example.com')
    reset_code1 = request_dict1['body'][19:25]
    fake_code1 = random_string(6)
    while fake_code1 == reset_code1:
        fake_code1 = random_string(6)
    # SETUP END

    with pytest.raises(ValueError):
        auth_passwordreset_reset(fake_code1, 'alsovalidpwd')

    # Check that invalid reset code attempt didn't invalidate reset_code1
    assert auth_passwordreset_reset(reset_code1, 'alsovalidpwd') == {}

def test_passwordreset_reset_invalid_password():
    # SETUP BEGIN
    reset_data()

    auth_register('user@example.com', 'validpassword', 'Test', 'User')
    auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')

    request_dict1 = auth_passwordreset_request('user@example.com')
    reset_code1 = request_dict1['body'][19:25]

    request_dict2 = auth_passwordreset_request('sabine.lim@unsw.edu.au')
    reset_code2 = request_dict2['body'][19:25]

    request_dict3 = auth_passwordreset_request('gamer@twitch.tv')
    reset_code3 = request_dict3['body'][19:25]
    # SETUP END

    with pytest.raises(ValueError):
        auth_passwordreset_reset(reset_code1, 'pwd')
    with pytest.raises(ValueError):
        auth_passwordreset_reset(reset_code2, 'pwd')
    with pytest.raises(ValueError):
        auth_passwordreset_reset(reset_code3, 'pwd')

    # Check that invalid password attempts didn't invalidate reset codes
    assert auth_passwordreset_reset(reset_code1, 'alsovalidpwd') == {}
    assert auth_passwordreset_reset(reset_code2, 'kindaAwesomeIGuess') == {}
    assert auth_passwordreset_reset(reset_code3, 'or_sitThat5fineT00') == {}
