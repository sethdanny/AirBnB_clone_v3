#!/usr/bin/python3
""" module to handle city routes """

from api.v1.views import app_views
from flask import request, jsonify, abort, make_response
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def cities_by_state_id(state_id):
    """ retrieve city objects for each state using state_id """
    if state_id is None:
        abort(404)

    st = storage.get(State, state_id)
    if st is None:
        abort(404)
    cts = st.cities
    return jsonify([ct.to_dict() for ct in cts])


@app_views.route('/cities/<city_id>/', methods=['GET'], strict_slashes=False)
def cities_by_cities_id(city_id):
    """ get all cities using their id """
    if city_id is None:
        abort(404)
    ct = storage.get(City, city_id)
    if ct is None:
        abort(404)
    return jsonify(ct.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def deleteCity(city_id=None):
    '''deletes a city'''
    if city_id is not None:
        res = storage.get(City, city_id)
        if res is not None:
            storage.delete(res)
            storage.save()
            return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'],
                 strict_slashes=False)
def postCity(state_id=None):
    '''posts a new city to a specific state'''
    if state_id is None:
        abort(404)
    st = storage.get(State, state_id)
    if st is None:
        abort(404)

    body = request.get_json()
    if body is None:
        abort(400, 'Not a JSON')
    if 'name' not in body.keys():
        abort(400, 'Missing name')
    body['state_id'] = st.id
    obj = City(**body)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def updateCity(city_id=None):
    '''updates a city'''
    if city_id is None:
        abort(404)
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)

    body = request.get_json()
    if body is None:
        abort(400, 'Not a JSON')
    for key in body.keys():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(obj, key, body[key])
    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)
