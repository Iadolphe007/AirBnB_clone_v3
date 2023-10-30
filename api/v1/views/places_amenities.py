#!/usr/bin/python3
"""places_amenities view"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.amenity import Amenity
import json
from os import environ


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def place_amenities(place_id):
    """return all amenitis present in a place"""
    env = environ.get('HBNB_TYPE_STORAGE')
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenityList = []
    if env == 'db':
        """db storage"""
        amenities = place.amenities
        for amenity in amenities:
            amenity = amenity.to_dict()
            amenityList.append(amenity)
    else:
        """file storage"""
        amenities = place.amenity_ids
        allamenities = storage.all(Amenity).values()
        for amenity in allamenities:
            if amenity.id in amenities:
                amenityList.append(amenity.to_dict())
    return jsonify(amenityList)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_amenity(place_id, amenity_id):
    """delete amenity"""
    env = environ.get('HBNB_TYPE_STORAGE')
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storageAmenity = storage.get(Amenity, amenity_id)
    if not storageAmenity:
        abort(404)
    if env == 'db':
        """database storage"""
        amenities = place.amenities
        for amenity in amenities:
            if amenity.id == amenity_id:
                storage.delete(amenity)
                storage.save()
                return make_response({}, 200)
        abort(404)
    else:
        """file storage"""
        amenities = place.amenity_ids
        if isinstance(amenities, str):
            amenities = json.loads(amenities)
        if amenity_id in amenities:
            amenities.remove(amenity_id)
            storage.save()
            return make_response({}, 200)
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST'])
def link_amenity(place_id, amenity_id):
    """Link amenity to a place"""
    env = environ.get('HBNB_TYPE_STORAGE')
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storageAmenity = storage.get(Amenity, amenity_id)
    if not storageAmenity:
        abort(404)
    if env == 'db':
        """database storage"""
        amenities = place.amenities
        for amenity in amenities:
            if amenity.id == amenity_id:
                return make_response(jsonify(amenity.to_dict()), 200)
        """link amenity"""
        amenities.append(storageAmenity)
        storage.save()
        return make_response(jsonify(storageAmenity.to_dict()), 201)
    else:
        """file storage"""
        amenities = place.amenity_ids
        if amenity_id in amenities:
            return make_response(jsonify(storageAmenity.to_dict()), 200)
        amenities.append(amenity_id)
        storage.save()
        return make_response(jsonify(storageAmenity.to_dict()), 201)
