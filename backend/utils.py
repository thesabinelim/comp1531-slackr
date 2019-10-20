# COMP1531 Project utils
# Written by Sabine Lim z5242579
# 16/10/19

import re
import random
import string

# Return True if email is valid, 0 otherwise.
def is_valid_email(email):
    email_re = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    return True if re.search(email_re, email) else False

# Return randomly generated string with given length. String can contain
# alphanumeric characters and special characters.
def random_string(length):
    characters = string.ascii_letters + string.digits + string.punctuation \
        + string.printable
    return ''.join(random.choice(characters) for _ in range(length))