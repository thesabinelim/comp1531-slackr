# COMP1531 Project utils
# Written by Sabine Lim z5242579
# 16/10/19

from re import search as re_search
from random import choice as random_choice
from string import ascii_lowercase, digits as ascii_digits
from urllib.parse import urlparse

# Return True if email is valid, 0 otherwise.
def is_valid_email(email):
    email_re = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    return True if re_search(email_re, email) else False

# Returns true if the url is not malformed
# https://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not
# e.g. 'google', 'http:/s', 'google.com' are malformed. 'http://google.com' is not
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False

# Return randomly generated string with given length. String can contain
# lowercase alphanumeric characters.
def random_string(length):
    characters = ascii_lowercase + ascii_digits
    return ''.join(random_choice(characters) for _ in range(length))
