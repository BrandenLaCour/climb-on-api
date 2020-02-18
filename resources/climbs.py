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

#Update route
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

#delete route
@climbs.route('/<id>', methods=['Delete'])
@login_required
def delete(id):
    payload = request.get_json()
    try:
        models.Climb.get(models.Climb.user == current_user.id)
        delete_query = models.Climb.delete().where(models.Climb.id == id)
        delete_query.execute()
       
        return jsonify(data={}, message='successfully deleted climb with id {}'.format(id), status=200),200

    except models.DoesNotExist:
        return jsonify(data={}, message='cannot delete climb, is not connected to user', status=200), 200

#show route
@climbs.route('/<id>', methods=['GET'])
def show_climb(id):
    climb = models.Climb.get_by_id(id)
    climb_dict = model_to_dict(climb)
    return jsonify(data=climb_dict, message='retrived climb {}'.format(climb_dict['name']), status=200), 200


@climbs.route('/member/<memberid>', methods=['GET'])
def get_members_climbs(memberid):
    member = models.User.get_by_id(memberid)
    member_dict = model_to_dict(member)
    climbs_dict = [model_to_dict(climb) for climb in member.climbs]
  
    return jsonify(data=climbs_dict, message='successfully retreived {} climbs from user {}'.format(len(climbs_dict), member_dict['username'] ), status=200),200

    