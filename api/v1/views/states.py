#!/usr/bin/python3
"""
    new view for State objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from datetime import datetime
import uuid


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    obj = storage.all(State).values()
    states_liste = [state.to_dict() for state in obj]
    return jsonify(states_liste)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states_id(state_id):
    obj = storage.get('State', 'state_id')
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict()), 'OK'


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_states(state_id):
     obj = storage.get(State, state_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
         abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def creating():
    answer = request.get_json()
    if not answer:
        abort(400, 'Not a JSON')
    if "name" not in answer:
        abort(400, {'Missing name'})
    obj = State(name=response['name'])
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), '201'


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def updating(state_id):
    obj = storage.get(State, state_id)
    if obj:
        if not request.get_json():
            abort(400, 'Not a JSON')

        data = request.get_json()
        ignored_data = ['id', 'created_at', 'updated_at']
        for loop1, loop2 in data.items():
            if loop1 not in ignored_data:
                setattr(obj, loop1, loop2)

        obj.save()
        return jsonify(obj.to_dict()), 200
    else:
        abort(404)
