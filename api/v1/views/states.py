#!/usr/bin/python3
"""state view"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
import json


@app_views.route('/states', strict_slashes=False)
def states():
    """Method to return all the states"""
    states = storage.all(State).values()
    stateList = []
    for state in states:
        newState = state.to_dict()
        stateList.append(newState)
    return jsonify(stateList)


@app_views.route('/states/<state_id>', strict_slashes=False)
def state(state_id):
    """retieves a single state GET"""
    states = storage.all(State).values()
    for state in states:
        newState = state.to_dict()
        id = newState.get('id')
        if id == state_id:
            return jsonify(newState)
    abort(404)


@app_views.route('/states/<sid>', strict_slashes=False, methods=['DELETE'])
def state_delete(sid):
    """Delete a state"""
    states = storage.all(State).values()
    for state in states:
        newState = state.to_dict()
        id = newState.get('id')
        if id == sid:
            storage.delete(state)
            storage.save()
            return make_response({}, 200)
    abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """saves a new instace of state to the database"""
    state = request.get_json()
    if not state:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif "name" not in state:
        return make_response(jsonify({"error": "Missing name"}), 400)
    newState = State(name=state['name'])
    storage.new(newState)
    storage.save()
    return make_response(jsonify(newState.to_dict()), 201)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    states = storage.all(State).values()
    data = {}
    for index, state in enumerate(states):
        if state.id == state_id:
            data = request.get_json()
            break
        if index == len(states) - 1:
            abort(404)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    keysAvoid = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in keysAvoid:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
