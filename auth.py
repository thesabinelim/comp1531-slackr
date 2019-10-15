from json import dumps
from flask import blueprint

auth_api = Blueprint('auth_api', __name__)

users = None

@auth_api.route('/auth/login', methods=['POST'])
def login():
    pass

@auth_api.route('/auth/logout', methods=['POST'])
def logout():
    pass
