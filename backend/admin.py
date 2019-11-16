# COMP1531 Project admin
# Written by Sabine Lim z5242579
# Refactored by Jake Tyler z5208823
# 22/10/19

from .db import Role, User, db_get_user_by_u_id
from .auth import validate_token
from .error import ValueError, AccessError

# Given user with id, set their permissions to new permissions described by
# permission_id.
# Return {}.
# Raise ValueError for invalid u_id or permission_id.
# Raise AccessError when user is not admin or owner.

# validates both users then returns the validated user and target
def admin_setup(token, target_id):
    
    u_id = validate_token(token)
    
    authorised_user = db_get_user_by_u_id(u_id)
    target = db_get_user_by_u_id(target_id)
    
    return authorised_user, target

# checks all errors
def admin_errors(target, permission_id, authorised_user):
    
    # if the target is non-existent
    if target is None:
        raise ValueError(description="User with u_id does not exist!")
    
    # if the permission id isnt an actual id
    if permission_id not in [perm.value for perm in Role]:
        raise ValueError(description="Invalid permission_id!")

    # if the user trying to change the permission does not have sufficient permissions to do so
    if authorised_user.get_slackr_role() != Role.owner \
        and authorised_user.get_slackr_role() != Role.admin:
        raise AccessError(description="Logged in user is not admin or owner!")
    
    # the target user has higher permissions
    if target.get_slackr_role().value < authorised_user.get_slackr_role().value:
        raise AccessError(description="Cannot modify permissions of a user with higher permissions")
    
    # changing the targets permissions to higher then the users.
    if permission_id < authorised_user.get_slackr_role().value:
        raise AccessError(description="Cannot modify permissions to be higher than authorised user's own permissions")

# authorises users, checks errors then changes and returns.
def admin_userpermission_change(token, target_id, permission_id):
    
    authorised_user, target = admin_setup(token, target_id)
    
    admin_errors(target, permission_id, authorised_user)

    target.set_slackr_role(Role(permission_id))

    return {}
