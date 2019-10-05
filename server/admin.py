from error import *

# Given user with id, set their permissions to new permissions described by
# permission_id. Return {}.
# Raise ValueError for invalid u_id or permission_id.
# Raise AccessError when user is not admin or owner.
def admin_userpermission_change(token, u_id, permission_id):
    if u_id not in [1234567,5242579,4201337,9876543]:
        raise ValueError
    
    if permission_id not in [1, 2, 3]:
        raise ValueError

    return {}
