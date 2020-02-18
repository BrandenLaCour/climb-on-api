from flask import Blueprint, jsonify, request
import models

from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

climbs = Blueprint('climbs', 'climbs')

#get all climbs
@climbs.route('/all', methods=['GET'])
def all_climbs():
    all_climbs = models.Climb.select()
    all_climbs_dict = [model_to_dict(climb) for climb in all_climbs]
    return jsonify(data=all_climbs_dict, message='successfully returned {} climbs'.format(len(all_climbs_dict)), status=200), 200

#create route
@climbs.route('/', methods=['POST'])
def create_climb():
    payload = request.get_json()
    payload = {**payload, "user": current_user.id}
    created_climb = models.Climb.create(**payload)
    created_climb_dict = model_to_dict(created_climb)
    created_climb_dict['user'].pop('password')
    return jsonify(data=created_climb_dict, message='successfully created climb {}'.format(created_climb_dict['name']), status=200), 200
