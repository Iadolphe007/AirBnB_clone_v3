#!/usr/bin/python3
"""amenity view"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity
import json


@app_views.route('/amenities', strict_slashes=False)
def amenities():
    """returns all amenities"""
    amenities = storage.all(Amenity)
    amenityList = []
    for amenity in amenities.values():
        amenityList.append(amenity.to_dict())
    return jsonify(amenityList)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def amenity(amenity_id):
    """returns a amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return (amenity.to_dict())


@app_views.route('/amenities/<id>', strict_slashes=False, methods=['DELETE'])
def amenity_delete(id):
    """Delete a amenity"""
    amenity = storage.get(Amenity, id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response({}, 200)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    """create a new amenity"""
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif "name" not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    newAmenity = Amenity(name=data['name'])
    storage.new(newAmenity)
    storage.save()
    return make_response(jsonify(newAmenity.to_dict()), 201)


@app_views.route('/amenities/<id>', strict_slashes=False, methods=['PUT'])
def update_amenity(id):
    """update amenity info"""
    amenity = storage.get(Amenity, id)
    if not amenity:
        abort(404)
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    keysAvoid = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in keysAvoid:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
