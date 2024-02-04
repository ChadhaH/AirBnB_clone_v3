#!/usr/bin/python3
"""
    variable app, instance of Flask
"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown(self):
    """closing"""
    storage.close()


@app.errorhandler(404)
def Not_Found(error):
    """error404 not found"""
    return jsonify('error'='Not found'), 404


if __name__ == '__main__':
    Host = getenv('HBNB_API_HOST', '0.0.0.0')
    Port = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=Host, port=Port, threaded=True)
