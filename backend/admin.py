# COMP1531 Project admin
# Written by Sabine Lim z5242579
# 22/10/19

from .db import Role, User, db_get_user_by_u_id
from .auth import validate_token
from .error import TokenError, AccessError

# Given user with id, set their permissions to new permissions described by
# permission_id.
# Return {}.
# Raise ValueError for invalid u_id or permission_id.
# Raise AccessError when user is not admin or owner.
def admin_userpermission_change(token, target_id, permission_id):
    u_id = validate_token(token)
    authorised_user = db_get_user_by_u_id(u_id)

    target = db_get_user_by_u_id(target_id)
    if target is None:
        raise ValueError("User with u_id does not exist!")
    
    if permission_id not in [Role.owner, Role.admin, Role.member]:
        raise ValueError("Invalid permission_id!")

    if authorised_user.get_slackr_role() != Role.owner \
        and authorised_user.get_slackr_role() != Role.admin:
        raise AccessError("Logged in user is not admin or owner!")

    if authorised_user.get_slackr_role() == Role.admin:
        if permission_id == Role.owner:
            raise AccessError("Admins cannot promote anyone to owner!")
        if target.get_slackr_role() == Role.owner:
            raise AccessError("Admins cannot modify permissions of owners!")

    target.set_role(permission_id)

    return {}
