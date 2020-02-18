from flask import Blueprint, jsonify, request
import models

from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

climbs = Blueprint('climbs', 'climbs')

@climbs.route('/', methods=['GET'])
def hello_world():
    print(request.get_json())
    return 'Hello World Climbs'

