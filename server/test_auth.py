# COMP1531 Project auth tests
# Written by Sabine Lim z5242579
# 29/09/19

import pytest

from auth import *

#######################
# auth_register Tests #
#######################

def test_auth_register_simple():
    regDict = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    assert regDict and 'u_id' in regDict and 'token' in regDict

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
    # SETUP END

    with pytest.raises(ValueError):
        auth_register('user@example.com', 'validpassword', 'Test', 'User')
    with pytest.raises(ValueError):
        auth_register('user@example.com', 'diffpassword', 'Test', 'User')

####################
# auth_login Tests #
####################

def test_auth_login_simple():
    # SETUP BEGIN
    regDict = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    # SETUP END

    loginDict = auth_login('user@example.com', 'validpassword')
    assert loginDict and 'u_id' in loginDict and 'token' in loginDict
    assert loginDict['u_id'] == regDict['u_id']

def test_auth_login_bademail():
    with pytest.raises(ValueError):
        auth_login('bademail', 'pwd')

def test_auth_login_notreg():
    with pytest.raises(ValueError):
        auth_login('idontexist@example.com', 'validpassword')

def test_auth_login_wrongpwd():
    # SETUP BEGIN
    regDict = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    # SETUP END

    with pytest.raises(ValueError):
        auth_login('user@example.com', 'wrongpassword')
