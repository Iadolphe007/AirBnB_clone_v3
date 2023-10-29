#!/usr/bin/python3
"""cities view"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City
import json


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def state_cities(state_id):
    """returns all the cities of a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    citiesList = []
    cities = state.cities
    for city in cities:
        citiesList.append(city.to_dict())
    return jsonify(citiesList)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def city(city_id):
    """returns a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return (city.to_dict())


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def city_delete(city_id):
    """Delete a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response({}, 200)


@app_views.route('/states/<id>/cities', strict_slashes=False, methods=['POST'])
def create_city(id):
    """create a new city for a state"""
    state = storage.get(State, id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif "name" not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    newCity = City(name=data['name'], state_id=state.id)
    storage.new(newCity)
    storage.save()
    return make_response(jsonify(newCity.to_dict()), 201)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """update city info"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    keysAvoid = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in keysAvoid:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
