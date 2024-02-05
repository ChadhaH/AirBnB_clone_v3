#!/usr/bin/python3
"""
    new view for Amenity objects that handles all default RESTFul API actions
"""

from flask import abort, jsonify, request
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities_all():
    liste = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in liste])


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def getting_amenity(amenity_id):
    liste = storage.get(Amenity, amenity_id)
    if liste:
        return jsonify(liste.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def deleting_amenity(amenity_id):
    liste = storage.get(Amenity, amenity_id)
    if liste:
        storage.delete(liste)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    if not request.get_json():
        abort(400, 'Not a JSON')

    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')
    liste  = Amenity(**data)
    liste.save()
    return jsonify(liste.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],strict_slashes=False)
def updating_amenity(amenity_id):
    liste = storage.get(Amenity, amenity_id)
    if liste:
        if not request.get_json():
            abort(400, 'Not a JSON')
        data = request.get_json()
        ignored_data = ['id', 'created_at', 'updated_at']
        for loop1, loop2 in data.items():
            if loop1 not in ignored_data:
                setattr(liste, loop1, loop2)
        liste.save()
        return jsonify(liste.to_dict()), 200
    else:
        abort(404)
