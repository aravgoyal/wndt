from flask import Blueprint
from flask import request, jsonify, make_response, current_app
from backend.db_connection import db

from db_files.models import Point
from db_files.database import db_session

from sqlalchemy import update, delete
from geoalchemy2 import Geometry

from flask_jwt_extended import jwt_required

# Create a new Blueprint for points
points = Blueprint('points', __name__)

# Create a new geo-referenced point
@points.route('/new', methods=['POST'])
@jwt_required()
def create_point():
    current_app.logger.info('POST /points route')
    info = request.json
    scenario_id = info.get('simulation_scenario_id')
    name = info.get('name')
    latitude = info.get('latitude')
    longitude = info.get('longitude')

    if not scenario_id or not name or not latitude or not longitude:
        return jsonify({"error": "Missing required fields"}), 400

    geom = Geometry(f'POINT({latitude} {longitude})', srid=4326)

    point = Point(
        scenario_id=scenario_id,
        name=name,
        geom=geom
    )

    db_session.add(point)
    db_session.commit()

    return make_response(jsonify({'message': 'Point created successfully!'}), 201)

# Get all geo-referenced points
@points.route('/view', methods=['GET'])
@jwt_required()
def get_all_points():
    current_app.logger.info('GET /points route')

    points = Point.query.all()

    return jsonify(points), 200

# Get all points for a specific simulation scenario
@points.route('/scenario/<int:scenario_id>', methods=['GET'])
@jwt_required()
def get_points_by_scenario(scenario_id):
    current_app.logger.info(f'GET /points/scenario/{scenario_id} route')

    points = Point.query.filter_by(scenario_id=scenario_id).all()

    return jsonify(points), 200

# Update a geo-referenced point
@points.route('/update/<int:point_id>', methods=['PUT'])
@jwt_required()
def update_point(point_id):
    current_app.logger.info(f'PUT /points/{point_id} route')
    point_info = request.json
    name = point_info.get('name')
    latitude = point_info.get('latitude')
    longitude = point_info.get('longitude')

    if not name or not latitude or not longitude:
        return jsonify({"error": "Missing required fields"}), 400

    geom = Geometry(f'POINT({latitude} {longitude})', srid=4326)
    updated = update(Point).where(Point.id == point_id).values(name=name, geom=geom)

    db_session.execute(updated)
    db_session.commit()

    return make_response(jsonify({'message': 'Point updated successfully!'}), 200)

# Delete a geo-referenced point
@points.route('/delete/<int:point_id>', methods=['DELETE'])
@jwt_required()
def delete_point(point_id):
    current_app.logger.info(f'DELETE /points/{point_id} route')

    deleted = delete(Point).where(Point.id == point_id)

    db_session.execute(deleted)
    db_session.commit()
    
    return make_response(jsonify({'message': 'Point deleted successfully!'}), 200)
