#!/usr/bin/python3
"""app module"""

from flask import Flask,jsonify
from api.v1.views import app_views
from models import storage
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_storage(obj):
    """call the close ()"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """return 404 as json"""
    response = jsonify({'error': 'Not Found'})
    return response


if __name__ == "__main__":
    """run only when executed as main"""
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
