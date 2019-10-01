# COMP1531 Project auth tests
# Written by Sabine Lim z5242579
# 29/09/19

import pytest

from auth import *

#######################
# auth_register Tests #
#######################

def test_auth_register_simple():
    regDict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    assert regDict1 and 'u_id' in regDict1 and 'token' in regDict1

    regDict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    assert regDict2 and 'u_id' in regDict2 and 'token' in regDict2
    # Check that registration attempts returned different values
    assert regDict2['u_id'] != regDict1['u_id'] and regDict2['token'] != regDict1['token']

    regDict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    assert regDict3 and 'u_id' in regDict3 and 'token' in regDict3
    # Check that registration attempts returned different values
    assert regDict3['u_id'] != regDict2['u_id'] and regDict3['token'] != regDict2['token']

def test_auth_register_bademail():
    with pytest.raises(ValueError):
        auth_register('bademail', 'validpassword', 'Test', 'User')

def test_auth_register_badpwd():
    with pytest.raises(ValueError):
        auth_register('user@example.com', 'pwd', 'Test', 'User')

def test_auth_register_badnames():
    with pytest.raises(ValueError):
        auth_register('user@example.com', 'validpassword',
            '123456789012345678901234567890123456789012345678901', 'User')
    with pytest.raises(ValueError):
        auth_register('user@example.com', 'validpassword', 'Test',
            '123456789012345678901234567890123456789012345678901')

def test_auth_register_emailtaken():
    # SETUP BEGIN
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
    regDict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    regDict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    regDict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    # SETUP END

    loginDict1 = auth_login('user@example.com', 'validpassword')
    assert loginDict1 and 'u_id' in loginDict1 and 'token' in loginDict1
    assert loginDict1['u_id'] == regDict1['u_id']

    loginDict2 = auth_login('sabine.lim@unsw.edu.au', 'ImSoAwes0me')
    assert loginDict2 and 'u_id' in loginDict2 and 'token' in loginDict2
    assert loginDict2['u_id'] == regDict2['u_id']

    loginDict3 = auth_login('gamer@twitch.tv', 'gamers_rise_up')
    assert loginDict3 and 'u_id' in loginDict3 and 'token' in loginDict3
    assert loginDict3['u_id'] == regDict3['u_id']

def test_auth_login_bademail():
    with pytest.raises(ValueError):
        auth_login('bademail', 'pwd')

def test_auth_login_notreg():
    with pytest.raises(ValueError):
        auth_login('idontexist@example.com', 'validpassword')

def test_auth_login_wrongpwd():
    # SETUP BEGIN
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
    regDict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    regDict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    regDict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    # SETUP END

    assert auth_logout(regDict1['token']) == {}
    assert auth_logout(regDict2['token']) == {}
    assert auth_logout(regDict3['token']) == {}

def test_auth_logout_badtoken():
    assert auth_logout('badtoken') == {}

####################################
# auth_passwordreset_request Tests #
####################################

# These tests will need to be written after auth_passwordreset_request gets
# actually implemented as right now it doesn't generate a reset token

def test_passwordreset_request_simple():
    # SETUP BEGIN
    regDict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    regDict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    regDict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    # SETUP END

    assert auth_passwordreset_request('user@example.com') == {}
    assert auth_passwordreset_request('sabine.lim@unsw.edu.au') == {}

##################################
# auth_passwordreset_reset Tests #
##################################

# These tests will need to be reworked once auth_passwordreset_request is
# actually implemented, as right now they're using hard coded reset tokens

def test_passwordreset_reset_simple():
    # SETUP BEGIN
    regDict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    regDict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    regDict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    # SETUP END

    assert auth_passwordreset_reset('abcdef', 'alsovalidpwd') == {}
    assert auth_passwordreset_reset('cfa027', 'kindaAwesomeIGuess') == {}
    assert auth_passwordreset_reset('bb809m', 'or_sitThat5fineT00') == {}

def test_passwordreset_reset_badpwd():
    # SETUP BEGIN
    regDict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    regDict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    regDict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    # SETUP END

    with pytest.raises(ValueError):
        auth_passwordreset_reset('abcdef', 'pwd')
    with pytest.raises(ValueError):
        auth_passwordreset_reset('cfa027', 'pwd')
    with pytest.raises(ValueError):
        auth_passwordreset_reset('bb809m', 'pwd')

