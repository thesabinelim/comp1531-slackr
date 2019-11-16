# COMP1531 Project admin
# Written by Sabine Lim z5242579
# 22/10/19

from .db import Role, User, db_get_user_by_u_id
from .auth import validate_token
from .error import ValueError, AccessError

# Given user with id, set their permissions to new permissions described by
# permission_id.
# Return {}.
# Raise ValueError for invalid u_id or permission_id.
# Raise AccessError when user is not admin or owner.

############################## Channel Setup ########################################

# main function, setup for readability
def admin_userpermission_change(token, target_id, permission_id):

    # sets up user and the target.
    authorised_user, target = admin_userpermission_change_setup(token, target_id)
    
    # error checks
    admin_userpermission_change_error(authorised_user, target, permission_id)

    # sets the required permission_id
    target.set_slackr_role(Role(permission_id))

    return {}

def admin_userpermission_change_setup(token, target_id):

    authorised_user = validate_token(token)
    
    target = db_get_user_by_u_id(target_id)

    return authorised_user, target

# error list
def admin_userpermission_change_error(authorised_user, target, permission_id):

    if permission_id not in [perm.value for perm in Role]:
        raise ValueError(description="Invalid permission_id!")
    
    if authorised_user.get_slackr_role() != Role.owner \
        and authorised_user.get_slackr_role() != Role.admin:
        raise AccessError(description="Logged in user is not admin or owner!")
    
    if target.get_slackr_role().value < authorised_user.get_slackr_role().value:
        raise AccessError(description="Cannot modify permissions of a user with higher permissions")
    
    if permission_id < authorised_user.get_slackr_role().value:
        raise AccessError(description="Cannot modify permissions to be higher than authorised user's own permissions")

