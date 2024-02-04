#!/usr/bin/python3
"""
    Index file
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


@app_views.route('/status', methods=['GET'])
def status_api():
    """
        API status
    """
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
def get_things():
    """
        number of retrieved objects
    """
    things = {
            'amenities': storage.count('Amenity'),
            'cities': storage.count('City'),
            'places': storage.count('Place'),
            'reviews': storage.count('Review'),
            'states': storage.count('State'),
            'users': storage.count('User')
            }
    return jsonify(things)

