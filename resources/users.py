from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict
from flask_login import current_user, logout_user, login_user

users = Blueprint('users', 'users')

@users.route('/', methods=['GET'])
def hello_world():
    return 'Hello World Users'