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
@login_required
def create_climb():
    payload = request.get_json()
    payload = {**payload, "user": current_user.id}
    created_climb = models.Climb.create(**payload)
    created_climb_dict = model_to_dict(created_climb)
    created_climb_dict['user'].pop('password')
    return jsonify(data=created_climb_dict, message='successfully created climb {}'.format(created_climb_dict['name']), status=200), 200

@climbs.route('/<id>', methods=['PUT'])
@login_required
def update_climb(id):
    payload = request.get_json()
    try:
        models.Climb.get(models.Climb.user == current_user.id)
        update_query = models.Climb.update(**payload).where(models.Climb.id == id)
        update_query.execute()
        updated_climb = models.Climb.get_by_id(id)
        updated_climb_dict = model_to_dict(updated_climb)
        return jsonify(data=updated_climb_dict, message='successfully update the climb {}'.format(updated_climb_dict['name']), status=200),200

    except models.DoesNotExist:
        return jsonify(data={}, message='cannot update climb, is not connected to user', status=200), 200
