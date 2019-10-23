# COMP1531 Project admin
# Written by Sabine Lim z5242579
# 22/10/19

from db import Role, User, db_get_user_by_u_id
from auth import validate_token
from error import TokenError, AccessError

# Given user with id, set their permissions to new permissions described by
# permission_id.
# Return {}.
# Raise ValueError for invalid u_id or permission_id.
# Raise AccessError when user is not admin or owner.
def admin_userpermission_change(token, u_id, permission_id):
    try:
        admin_id, token_valid = validate_token(token)
    except ValueError:
        raise ValueError("Token was not generated by server!")
    if not token_valid:
        raise TokenError("Token is invalid!")

    admin = db_get_user_by_u_id(admin_id)
    target = db_get_user_by_u_id(u_id)
    if target == None:
        raise ValueError("User with u_id does not exist!")
    
    if permission_id not in [Role.owner, Role.admin, Role.member]:
        raise ValueError("Invalid permission_id!")

    if admin.get_slackr_role() != Role.owner and admin.get_slackr_role() != Role.admin:
        raise AccessError("Logged in user is not admin or owner!")

    if admin.get_slackr_role() == Role.admin:
        if permission_id == Role.owner:
            raise AccessError("Admins cannot promote anyone to owner!")
        if target.get_slackr_role() == Role.owner:
            raise AccessError("Admins cannot modify permissions of owners!")

    target.set_role(permission_id)

    return {}
