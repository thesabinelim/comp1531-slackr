# COMP1531 Project auth tests
# Written by Sabine Lim z5242579
# 29/09/19

from auth import *

def test_auth_register_login_simple():
    response = auth_login("user@example.com", "123456")
    assert response and 'u_id' response and 'token' in response
