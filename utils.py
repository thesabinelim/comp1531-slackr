# COMP1531 Project utils
# Written by Sabine Lim z5242579
# 16/10/19

import re

# Return True if email is valid, 0 otherwise
def is_valid_email(email):
    email_re = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    return True if re.search(email_re, email) else False
