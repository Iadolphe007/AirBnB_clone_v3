#!/usr/bin/python3
"""places view"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
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


@app_views.route('/places_search', strict_slashes=False, methods=['POST'])
def search_place():
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    sList = data.get('states')
    cList = data.get('cities')
    aList = data.get('amenities')
    placesList = []
    placesWithAmenities = []
    if (not data or (not sList and not cList and not aList)):
        places = storage.all(Place).values()
        for place in places:
            placesList.append(place.to_dict())
        return jsonify(placesList)
    if sList:
        for stateId in sList:
            state = storage.get(State, stateId)
            if not state:
                abort(404)
            cities = state.cities
            for city in cities:
                places = city.places
                for place in places:
                    placesList.append(place.to_dict())
    if cList:
        for cityId in cList:
            city = storage.get(City, cityId)
            if not city:
                abort(404)
            places = city.places
            for place in places:
                place = place.to_dict()
                if place not in placesList:
                    placesList.append(place)
    if aList:
        """check if each plave in placesList has all required amenities
        in aList"""
        for place in placesList:
            place_id = place.get('id')
            dbplace = storage.get(Place, place_id)
            amenities = dbplace.amenities
            for amenity in amenities:
                if amenity.id in aList and place not in placesWithAmenities:
                    placesWithAmenities.append(place)
        return jsonify(placesWithAmenities)
    return jsonify(placesList)
