# COMP1531 Project auth tests
# Written by Jiacheng Lu z5230596
# 03/10/19

import pytest

from admin import *

##############################
# admin_userpermission Tests #
##############################


def test_adminpermission_simple():
    token1 = 1231231
    u_id1 = 1234567
    permission1 = admin_userpermission_change(token1,u_id1,2)%10
    assert permission1 == 2

    token2 = 1231232
    u_id2 = 5242579
    permission2 = admin_userpermission_change(token2,u_id2,1)%10
    assert permission2 == 1

def test_adminpermission_invaild_uid():
    token1 = 1231231
    u_id1 = 12345
    with pytest.raises(ValueError):
        admin_userpermission_change(token1,u_id1,1)

    token2 = 1231232
    u_id2 = 5242
    with pytest.raises(ValueError):
        admin_userpermission_change(token2,u_id2,2)
    
def test_adminpermission_invaild_permissionid():
    token1 = 1231231
    u_id1 = 1234567
    permission1 = admin_userpermission_change(token1,u_id1,2)%10
    assert permission1 == 2

    token2 = 1231232
    u_id2 = 5242579
    permission2 = admin_userpermission_change(token2,u_id2,1)%10
    assert permission2 == 1

    token1 = 1231231
    u_id1 = 1234567
    with pytest.raises(ValueError):
        admin_userpermission_change(token1,u_id1,4)

    token2 = 1231232
    u_id2 = 5242579
    with pytest.raises(ValueError):
        admin_userpermission_change(token2,u_id2,1235)

def test_adminpermission_as_a_member():
    token1 = 1231233
    u_id1 = 1234567
    with pytest.raises(AccessError):
        admin_userpermission_change(token1,u_id1,1)
