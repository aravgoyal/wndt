from flask import Blueprint
from flask import request, jsonify, make_response, current_app
from backend.db_connection import db

from backend.db_files.models import Scenario
from backend.db_files.database import db_session

from sqlalchemy import update, delete
from geoalchemy2 import Geometry
from shapely.geometry import Point, mapping

from flask_jwt_extended import jwt_required

# Create a new Blueprint for scenarios
scenarios = Blueprint('scenarios', __name__)

# Create a new simulation scenario
@scenarios.route('/new', methods=['POST'])
@jwt_required()
def create_scenario():
    current_app.logger.info('POST /scenarios route')
    scenario_info = request.json
    visibility = scenario_info.get('visibility')
    frequency = scenario_info.get('frequency')
    scenario_type = scenario_info.get('scenario_type')
    map_center_long = scenario_info.get('map_center_long'),
    map_center_lat = scenario_info.get('map_center_lat'),
    map_size = scenario_info.get('map_size')
    user_id = scenario_info.get('user_id')

    if not visibility or not user_id:
        return jsonify({"error": "Missing required fields"}), 400

    point = Point(map_center_long, map_center_lat)
    geojson = mapping(point)

    scenario = Scenario(
        visibility=visibility,
        frequency=frequency,
        scenario_type=scenario_type,
        map_center=geojson,
        map_size=map_size,
        user_id=user_id
    )

    db_session.add(scenario)
    db_session.commit()

    return make_response(jsonify({'message': 'Scenario created successfully!'}), 201)

# Get all simulation scenarios
@scenarios.route('/view', methods=['GET'])
@jwt_required()
def get_all_scenarios():
    current_app.logger.info('GET /scenarios route')

    scenarios = Scenario.query.all()
    scenarios_dict = [scenario.as_dict() for scenario in scenarios]

    return jsonify(scenarios_dict), 200

# Get a specific simulation scenario by ID
@scenarios.route('/view/<int:scenario_id>', methods=['GET'])
@jwt_required()
def get_scenario_by_id(scenario_id):
    current_app.logger.info(f'GET /scenarios/{scenario_id} route')

    scenario = Scenario.query.filter_by(id=scenario_id).first()

    if scenario:
        return jsonify(scenario.as_dict()), 200

    return jsonify({"error": "Scenario not found"}), 404

# Update a simulation scenario
@scenarios.route('/update/<int:scenario_id>', methods=['PUT'])
@jwt_required()
def update_scenario(scenario_id):
    current_app.logger.info(f'PUT /scenarios/{scenario_id} route')
    scenario_info = request.json
    visibility = scenario_info.get('visibility')
    frequency = scenario_info.get('frequency')
    scenario_type = scenario_info.get('scenario_type')
    map_center = scenario_info.get('map_center')
    map_size = scenario_info.get('map_size')

    if not visibility:
        return jsonify({"error": "Missing required fields"}), 400

    updated = update(Scenario).where(Scenario.id == scenario_id).values(visibility=visibility, frequency=frequency, scenario_type=scenario_type, map_center=map_center, map_size=map_size)
    db_session.execute(updated)
    db_session.commit()
    
    return make_response(jsonify({'message': 'Scenario updated successfully!'}), 200)

# Delete a simulation scenario
@scenarios.route('/delete/<int:scenario_id>', methods=['DELETE'])
@jwt_required()
def delete_scenario(scenario_id):
    current_app.logger.info(f'DELETE /scenarios/{scenario_id} route')

    deleted = delete(Scenario).where(Scenario.id == scenario_id)
    db_session.execute(deleted)
    db_session.commit()
    
    return make_response(jsonify({'message': 'Scenario deleted successfully!'}), 200)
