from flask import Blueprint
from flask import request, jsonify, make_response, current_app
from backend.db_connection import db

# Create a new Blueprint for scenarios
scenarios = Blueprint('scenarios', __name__)

# Create a new simulation scenario
@scenarios.route('/new', methods=['POST'])
def create_scenario():
    current_app.logger.info('POST /scenarios route')
    scenario_info = request.json
    visibility = scenario_info.get('visibility')
    frequency = scenario_info.get('frequency')
    scenario_type = scenario_info.get('type')
    map_center_lat = scenario_info.get('map_center_lat')
    map_center_long = scenario_info.get('map_center_long')
    map_size = scenario_info.get('map_size')
    user_id = scenario_info.get('user_id')

    if not visibility or not user_id:
        return jsonify({"error": "Missing required fields"}), 400

    query = '''
        INSERT INTO SimulationScenarios (visibility, frequency, type, map_center_lat, map_center_long, map_size, user_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    data = (visibility, frequency, scenario_type, map_center_lat, map_center_long, map_size, user_id)

    cursor = db.cursor()
    cursor.execute(query, data)
    scenario_id = cursor.lastrowid
    db.commit()
    cursor.close()
    db.close()

    return make_response(jsonify({'message': 'Scenario created successfully!', 'scenario_id': scenario_id}), 201)

# Get all simulation scenarios
@scenarios.route('/view', methods=['GET'])
def get_all_scenarios():
    current_app.logger.info('GET /scenarios route')

    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM SimulationScenarios')
    scenarios = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(scenarios), 200

# Get a specific simulation scenario by ID
@scenarios.route('/view/<int:scenario_id>', methods=['GET'])
def get_scenario_by_id(scenario_id):
    current_app.logger.info(f'GET /scenarios/{scenario_id} route')

    cursor = db.cursor(dictionary=True)
    query = 'SELECT * FROM SimulationScenarios WHERE id = %s'
    cursor.execute(query, (scenario_id,))
    scenario = cursor.fetchone()

    if scenario:
        cursor.close()
        db.close()
        return jsonify(scenario), 200

    cursor.close()
    db.close()
    return jsonify({"error": "Scenario not found"}), 404

# Update a simulation scenario
@scenarios.route('/update/<int:scenario_id>', methods=['PUT'])
def update_scenario(scenario_id):
    current_app.logger.info(f'PUT /scenarios/{scenario_id} route')
    scenario_info = request.json
    visibility = scenario_info.get('visibility')
    frequency = scenario_info.get('frequency')
    scenario_type = scenario_info.get('type')
    map_center_lat = scenario_info.get('map_center_lat')
    map_center_long = scenario_info.get('map_center_long')
    map_size = scenario_info.get('map_size')

    if not visibility:
        return jsonify({"error": "Missing required fields"}), 400

    query = '''
        UPDATE SimulationScenarios
        SET visibility = %s, frequency = %s, type = %s, map_center_lat = %s, map_center_long = %s, map_size = %s
        WHERE id = %s
    '''
    data = (visibility, frequency, scenario_type, map_center_lat, map_center_long, map_size, scenario_id)

    cursor = db.cursor()
    cursor.execute(query, data)
    db.commit()

    if cursor.rowcount == 0:
        cursor.close()
        db.close()
        return jsonify({"error": "Scenario not found"}), 404

    cursor.close()
    db.close()
    return make_response(jsonify({'message': 'Scenario updated successfully!'}), 200)

# Delete a simulation scenario
@scenarios.route('/delete/<int:scenario_id>', methods=['DELETE'])
def delete_scenario(scenario_id):
    current_app.logger.info(f'DELETE /scenarios/{scenario_id} route')

    query = 'DELETE FROM SimulationScenarios WHERE id = %s'
    cursor = db.cursor()
    cursor.execute(query, (scenario_id,))
    db.commit()

    if cursor.rowcount == 0:
        cursor.close()
        db.close()
        return jsonify({"error": "Scenario not found"}), 404

    cursor.close()
    db.close()
    return make_response(jsonify({'message': 'Scenario deleted successfully!'}), 200)
