#!/usr/bin/python3
"""User view"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User
import json


@app_views.route('/users', strict_slashes=False)
def users():
    """returns all users"""
    users = storage.all(User)
    userList = []
    for user in users.values():
        userList.append(user.to_dict())
    return jsonify(userList)


@app_views.route('/users/<user_id>', strict_slashes=False)
def user(user_id):
    """returns a user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return (user.to_dict())


@app_views.route('/users/<id>', strict_slashes=False, methods=['DELETE'])
def user_delete(id):
    """Delete a user"""
    user = storage.get(User, id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response({}, 200)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """create a new user"""
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif "email" not in data:
        return make_response(jsonify({"error": "Missing email"}), 400)
    elif "password" not in data:
        return make_response(jsonify({"error": "Missing password"}), 400)
    newUser = User(email=data['email'], password=data['password'])
    storage.new(newUser)
    storage.save()
    return make_response(jsonify(newUser.to_dict()), 201)


@app_views.route('/users/<id>', strict_slashes=False, methods=['PUT'])
def update_user(id):
    """update user info"""
    user = storage.get(User, id)
    if not user:
        abort(404)
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    keysAvoid = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in keysAvoid:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
