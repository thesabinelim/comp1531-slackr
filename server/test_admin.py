# COMP1531 Project auth tests
# Written by Jiacheng Lu z5230596
# 03/10/19

import pytest

from admin import *

##############################
# admin_userpermission Tests #
##############################

def test_adminpermission_simple():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    reg_dict3 = auth_register('gamer@twitch.tv', 'gamers_rise_up', 'Gabe', 'Newell')
    # SETUP END

    # Test promotes Sabine to admin
    assert admin_userpermission_change(reg_dict1['token'], reg_dict2['u_id'], 2) == {}

    # Sabine promotes Gabe to admin
    assert admin_userpermission_change(reg_dict2['token'], reg_dict3['u_id'], 2) == {}

    # Test promotes Sabine to owner
    assert admin_userpermission_change(reg_dict1['token'], reg_dict2['u_id'], 1) == {}

    # Sabine demotes Test to admin
    assert admin_userpermission_change(reg_dict2['token'], reg_dict1['u_id'], 2) == {}

    # Test demotes Gabe to user
    assert admin_userpermission_change(reg_dict1['token'], reg_dict3['u_id'], 3) == {}

def test_adminpermission_bad_uid():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    # SETUP END

    with pytest.raises(ValueError):
        admin_userpermission_change(reg_dict1['token'], reg_dict1['u_id'] + 1, 1)
    
def test_adminpermission_bad_permissionid():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    # SETUP END

    with pytest.raises(ValueError):
        admin_userpermission_change(reg_dict1['token'], reg_dict2['u_id'],4)

    with pytest.raises(ValueError):
        admin_userpermission_change(reg_dict1['token'], reg_dict2['u_id'], 0)

def test_adminpermission_noperms():
    # SETUP BEGIN
    reg_dict1 = auth_register('user@example.com', 'validpassword', 'Test', 'User')
    reg_dict2 = auth_register('sabine.lim@unsw.edu.au', 'ImSoAwes0me', 'Sabine', 'Lim')
    # SETUP END

    # Sabine tries to demote Test to admin
    with pytest.raises(AccessError):
        admin_userpermission_change(reg_dict2['token'], reg_dict1['u_id'], 2)

    # Sabine tries to promote herself to admin
    with pytest.raises(AccessError):
        admin_userpermission_change(reg_dict2['token'], reg_dict2['u_id'], 2)

    # Test promotes Sabine to owner
    assert admin_userpermission_change(reg_dict1['token'], reg_dict1['u_id'], 2) == {}

    # Sabine tries to promote herself to owner
    with pytest.raises(AccessError):
        admin_userpermission_change(reg_dict2['token'], reg_dict2['u_id'], 1)

    # Sabine tries to demote Test to admin
    with pytest.raises(AccessError):
        admin_userpermission_change(reg_dict2['token'], reg_dict1['u_id'], 2)
