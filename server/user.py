# COMP1531 Project User
# Written by Bridget McCarthy z5255505
# 02/10/19

import re


# Helper function during testing to see if a token is valid.
# Doesn't actually work yet.
def token_valid(token):
    if token == "56789" or token == "valid_token":
        return True
    else:
        return False

# For a valid user, returns information about their email, first name, last 
# name, and handle.
# Raises a ValueError when the u_id is not a valid user.
# Returns a dictionary of user information.
def user_profile(token, u_id):
    if not token_valid(token):
        raise AccessError
    if u_id < 0:
        raise ValueError
    return { 
        "email": f"{u_id}@example.com",
        "name_first": "Bob", 
        "name_last": "Adams",
        "handle_str": f"{u_id}"
    }

# Update the authorised user's first and last name
def user_profile_setname(token, name_first, name_last):
    if not token_valid(token):
        raise AccessError
    if len(name_first) > 50 or len(name_last) > 50:
        raise ValueError

# Update the authorised user's email address
def user_profile_setemail(token, email):
    if not token_valid(token):
        raise AccessError
    if not valid_email(email):
        raise ValueError
    # if email in use:
    #    raise ValueError
    if email == 'usedemail@example.com':
        raise ValueError

# Update the authorised user's handle (i.e. display name)
def user_profile_sethandle(token, handle_str):
    if not token_valid(token):
        raise AccessError
    if len(handle_str) > 20:
        raise ValueError

# Given a URL of an image on the internet, crops the image within bounds 
# (x_start, y_start) and (x_end, y_end). Position (0,0) is the top left.
def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    if not token_valid(token):
        raise AccessError
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


      
# Validates an email by regular expression
# # https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
def valid_email(email):  
    # Make a regular expression 
    # for validating an Email 
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    # pass the regualar expression 
    # and the string in search() method 
    if(re.search(regex,email)):  
        return True
          
    else:  
        return False