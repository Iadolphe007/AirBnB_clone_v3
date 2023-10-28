#!/usr/bin/python3
"""module comtaining endpoint"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage

#app = Flask(__name__)


@app_views.route('/status', strict_slashes=False)
def status():
    """return json status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def count():
    """retrieves object number by type"""
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
