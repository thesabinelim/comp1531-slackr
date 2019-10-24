# COMP1531 Project db
# Written by Bridget McCarthy z5255505
# 24/10/19

from json import dumps
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

##################
# Error Handling #
##################

# As recommended by the course, error handling will be handled similarly to
# https://gitlab.cse.unsw.edu.au/COMP1531/19T3-lectures/blob/master/helper/myexcept.py
# Exceptions are raised as:
# ValueError(description="error message here")
# This is converted into json for the frontend to show nicely.
def default_handler(err):
    response = err.get_response()
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description()
    })
    response.content_type = 'application/json'
    return response


class ValueError(HTTPException):
    code = 400
    message = "No message specified"

class AccessError(HTTPException):
    code = 403
    message = "No message specified"

class TokenError(Exception):
    code = 401
    message = "No message specified"
