from flask import Blueprint, jsonify, request
import models

from playhouse.shortcuts import model_to_dict
from flask_login import current_user, logout_user, login_user
from flask_bcrypt import generate_password_hash, check_password_hash

users = Blueprint('users', 'users')

@users.route('/register', methods=['POST'])
def register():
   
    payload = request.get_json()

    try:
        models.User.get(models.User.username == payload['username'])
        models.User.get(models.User.email == payload['email'])
        return jsonify(data={}, message='username or email already exists', status=200), 200

    except models.DoesNotExist:
        created_user = models.User.create(**payload)
        created_user.password = generate_password_hash(payload['password'])
        created_user.save()
        created_user_dict = model_to_dict(created_user)
        created_user_dict.pop('password')

        return jsonify(data=created_user_dict, message='succesfully created user {}'.format(created_user_dict['username']), status=200), 200

        

@users.route('/login', methods=["POST"])
def login():
    payload = request.get_json()
    print(payload)
    try:
        user = models.User.get(models.User.username == payload['username'])
        user_dict = model_to_dict(user)
        password_good = check_password_hash(user.password, payload['password'])
        if password_good:
            login_user(user)
            return jsonify(data=user_dict, message='{} logged in successfully'.format(user_dict['username']), status=200), 200
        else:
            return jsonify(data={}, message='username or password incorrect', status=200), 200
    except models.DoesNotExist:
        return jsonify(data={}, message='username or password incorrect', status=200), 200

@users.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return jsonify(data={}, message='logged out successfully', status=200), 200

@users.route('/all', methods=['GET'])
def get_users():
    all_users = models.User.select()
    all_users_dict = [model_to_dict(user) for user in all_users]
    return jsonify(data=all_users_dict, message=f"successfully retrieved {len(all_users_dict)} users", status=200), 200
