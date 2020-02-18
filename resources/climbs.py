from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

climbs = Blueprint('climbs', 'climbs')

@climbs.route('/', methods=['GET'])
def hello_world():
    return 'Hello World Climbs'