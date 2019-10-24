# COMP1531 Project User
# Written by Bridget McCarthy z5255505
# 02/10/19

import re

from .db import User, db_get_user_by_u_id, db_get_user_by_email, db_get_user_by_handle
from .auth import validate_token
from .utils import is_valid_email

# For a valid user, returns information about their email, first name, last 
# name, and handle.
# Raises a ValueError when the u_id is not a valid user.
# Returns a dictionary of user information.
def user_profile(token, target_u_id):
    validate_token(token)

    target_user = db_get_user_by_u_id(target_u_id)
    if target_user is None:
        raise ValueError("User does not exist")

    return { 
        "email": target_user.get_email(),
        "name_first": target_user.get_first_name(), 
        "name_last": target_user.get_last_name(),
        "handle_str": target_user.get_handle()
    }

# Update the authorised user's first and last name
def user_profile_setname(token, name_first, name_last):
    u_id = validate_token(token)
    user = db_get_user_by_u_id(u_id)

    if len(name_first) < 1 or len(name_first) > 50:
        raise ValueError("First name not between 1 and 50 characters")
    if len(name_last) < 1 or len(name_last) > 50:
        raise ValueError("Last name not between 1 and 50 characters")

    user.set_first_name(name_first)
    user.set_first_name(name_last)

    return {}

# Update the authorised user's email address
def user_profile_setemail(token, email):
    u_id = validate_token(token)
    user = db_get_user_by_u_id(u_id)

    if not is_valid_email(email):
        raise ValueError("Email invalid")
    if db_get_user_by_email(email) is not None:
        raise ValueError("Email already in use")

    user.set_email(email)

    return {}

# Update the authorised user's handle (i.e. display name)
def user_profile_sethandle(token, handle_str):
    u_id = validate_token(token)
    user = db_get_user_by_u_id(u_id)

    if len(handle_str) < 3 or len(handle_str) > 20:
        raise ValueError("Handle not between 3 and 20 characters")
    if db_get_user_by_handle(handle_str) is not None:
        raise ValueError("Handle is already in use")

    user.set_handle(handle_str)

    return {}


# NOTE: Not to be implemented until iteration 3 according to spec!!!
# Given a URL of an image on the internet, crops the image within bounds 
# (x_start, y_start) and (x_end, y_end). Position (0,0) is the top left.
def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    # Need to get http status of img_url
    # For now these are just test values
    http_return = 200
    img_width = 200
    img_height = 200
    if http_return != 200:
        raise ValueError
    if x_start < 0 or x_start > img_width or x_end < 0 or x_end > img_width:
        raise ValueError
    if y_start < 0 or y_start > img_height or y_end < 0 or y_end > img_height:
        raise ValueError
