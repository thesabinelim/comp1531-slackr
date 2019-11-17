# COMP1531 Project users
# Written by Sabine Lim z5242579
# 06/11/19

from .auth import validate_token
from .db import User, db_get_all_users

############################## Users All ########################################

# Returns dictionary containing list of all users in Slackr.
def users_all(token):
    validate_token(token)
    return {'users': [user.to_dict() for user in db_get_all_users()]}
