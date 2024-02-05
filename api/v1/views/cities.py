#!/usr/bin/python3
"""
    create a new view for City objects that handles all default RESTFul API actions
"""

from flask import abort, jsonify, request
from models.state import State
from models.city import City
from api.v1.views import app_views
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],strict_slashes=False)
    def cities_by_states(state_id):
        obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    city = [city.to_dict() for city in obj.city]
    return jsonify(city)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def getting_city(city_id):
        City = storage.get(City, city_id)
    if City:
        return jsonify(City.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def deleting_city(city_id):
    City = storage.get(City, city_id)
    if City:
        storage.delete(City)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],strict_slashes=False)
def creating_city(state_id):
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    states = storage.all("State").values()
    objs = [obj.to_dict() for obj in objs if obj.id == state_id]
    if objs == []:
        abort(404)
    Cities = []
    new_c = City(name=request.json['name'], state_id=state_id)
    storage.new(new_c)
    storage.save()
    Cities.append(new_c.to_dict())
    return jsonify(Cities[0]), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def updating_city(city_id):
    City = storage.get(City, city_id)
    if City:
        if not request.get_json():
            abort(400, 'Not a JSON')

        data = request.get_json()
        ignored_data = ['id', 'state_id', 'created_at', 'updated_at']
        for loop1, loop2 in data.items():
            if loop1 not in ignored_data:
                setattr(City, loop1, loop2)

        City.save()
        return jsonify(City.to_dict()), 200
    else:
        abort(404)
