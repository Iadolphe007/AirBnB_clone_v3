#!/usr/bin/python3
"""places view"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.place import Place
from models.user import User
import json


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def city_places(city_id):
    """returns all the places of a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    placesList = []
    places = city.places
    for city in places:
        placesList.append(city.to_dict())
    return jsonify(placesList)


@app_views.route('/places/<place_id>', strict_slashes=False)
def place(place_id):
    """returns a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return (place.to_dict())


@app_views.route('/places/<id>', strict_slashes=False, methods=['DELETE'])
def place_delete(id):
    """Delete a place"""
    place = storage.get(Place, id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response({}, 200)


@app_views.route('/cities/<id>/places', strict_slashes=False, methods=['POST'])
def create_place(id):
    """create a new place for a city"""
    city = storage.get(City, id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif "user_id" not in data:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    elif "name" not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    newPlace = Place(user_id=data['user_id'],
                     city_id=city.id, name=data['name'])
    storage.new(newPlace)
    storage.save()
    return make_response(jsonify(newPlace.to_dict()), 201)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    """update place info"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    keysAvoid = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in keysAvoid:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
