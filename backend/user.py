# COMP1531 Project User
# Written by Bridget McCarthy z5255505
# 02/10/19

import re

from .db import User, db_get_user_by_u_id, db_get_user_by_email, db_get_user_by_handle, db_get_backend_url
from .auth import validate_token
from .utils import is_valid_email, random_string, is_valid_url
from .error import ValueError
import os

# Python Image Processing library for upload photo
# use 'pip install Pillow' and 'pip install requests'
from PIL import Image
import requests
from io import BytesIO

# For a valid user, returns information about their email, first name, last 
# name, and handle.
# Raises a ValueError when the u_id is not a valid user.
# Returns a dictionary of user information.
def user_profile(token, target_u_id):
    validate_token(token)

    target_user = db_get_user_by_u_id(target_u_id)
    if target_user is None:
        raise ValueError(description="User does not exist")

    return target_user.to_dict()

# Update the authorised user's first and last name
def user_profile_setname(token, name_first, name_last):
    u_id = validate_token(token)
    user = db_get_user_by_u_id(u_id)

    if len(name_first) < 1 or len(name_first) > 50:
        raise ValueError(description="First name not between 1 and 50 characters")
    if len(name_last) < 1 or len(name_last) > 50:
        raise ValueError(description="Last name not between 1 and 50 characters")

    user.set_first_name(name_first)
    user.set_last_name(name_last)

    return {}

# Update the authorised user's email address
def user_profile_setemail(token, email):
    u_id = validate_token(token)
    user = db_get_user_by_u_id(u_id)

    if not is_valid_email(email):
        raise ValueError(description="Email invalid")
    if db_get_user_by_email(email) is not None:
        raise ValueError(description="Email already in use")

    user.set_email(email)

    return {}

# Update the authorised user's handle (i.e. display name)
def user_profile_sethandle(token, handle_str):
    u_id = validate_token(token)
    user = db_get_user_by_u_id(u_id)

    if len(handle_str) < 3 or len(handle_str) > 20:
        raise ValueError(description="Handle not between 3 and 20 characters")
    if db_get_user_by_handle(handle_str) is not None:
        raise ValueError(description="Handle is already in use")

    user.set_handle(handle_str)

    return {}


# Given a URL of an image on the internet, crops the image within bounds 
# (x_start, y_start) and (x_end, y_end). Position (0,0) is the top left.
# After processing this image is stored locally on the server, and the 
# profile_img_url is a url to the server
def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    u_id = validate_token(token)
    user = db_get_user_by_u_id(u_id)

    # Validate url, as requests does not work with malformed urls
    if not is_valid_url(img_url):
        raise ValueError(description=f"img_url is a malformed URL!")

    # https://stackoverflow.com/questions/7391945/how-do-i-read-image-data-from-a-url-in-python
    response = None
    try:
        response = requests.get(img_url)
    except Exception as e:
        raise ValueError(description=f"img_url is invalid!")
    if response.status_code != 200:
        raise ValueError(description=f"img_url returned HTTP {response.status_code}!")

    # Attempt to load the image
    img = None
    try:
        img = Image.open(BytesIO(response.content))
    except IOError as e:
        raise ValueError(description="URL is not an image!")
    img_width, img_height = img.size
    if img.format != "JPEG":
        raise ValueError(description="Image is not a JPEG!")
    if x_start < 0 or x_start > img_width or x_end < 0 or x_end > img_width:
        raise ValueError(description="X is out of bounds of image")
    if y_start < 0 or y_start > img_height or y_end < 0 or y_end > img_height:
        raise ValueError(description="Y is out of bounds of image")
    if x_end <= x_start or y_end <= y_start:
        raise ValueError(description="End coordinates are before the start coordinates")

    # Crop the image
    cropped_image = img.crop([x_start, y_start, x_end, y_end])
    if not os.path.exists('imgurls'):
        os.makedirs('imgurls')

    image_folder = 'imgurls'
    randstr = random_string(20)
    filepath = f"{image_folder}/{user.get_u_id()}_{randstr}.jpg"
    while os.path.exists(f"{filepath}"):
        randstr = random_string(20)
        filepath = f"{image_folder}/{user.get_u_id()}_{randstr}.jpg"
    cropped_image.save(filepath)

    # Set the user's profile_img_url to this new cropped image
    # This is just relative to local storage, and usage appends the url
    backend_url = db_get_backend_url()
    
    user.set_profile_img_url(f'{backend_url}{filepath}')
