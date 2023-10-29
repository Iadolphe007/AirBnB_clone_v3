#!/usr/bin/python3
"""app module"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_storage(obj):
    """call the close ()"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    response = jsonify({'error': 'Not Found'})
    return response


if __name__ == "__main__":
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
