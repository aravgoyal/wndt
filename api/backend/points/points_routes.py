from flask import Blueprint
from flask import request, jsonify, make_response, current_app
from backend.db_connection import db

from flask_jwt_extended import jwt_required

# Create a new Blueprint for points
points = Blueprint('points', __name__)

# Create a new geo-referenced point
@points.route('/new', methods=['POST'])
@jwt_required()
def create_point():
    current_app.logger.info('POST /points route')
    point_info = request.json
    name = point_info.get('name')
    latitude = point_info.get('latitude')
    longitude = point_info.get('longitude')
    scenario_id = point_info.get('simulation_scenario_id')

    if not name or not latitude or not longitude or not scenario_id:
        return jsonify({"error": "Missing required fields"}), 400

    query = '''
        INSERT INTO GeoReferencedPoints (name, latitude, longitude, simulation_scenario_id)
        VALUES (%s, %s, %s, %s)
    '''
    data = (name, latitude, longitude, scenario_id)

    cursor = db.cursor()
    cursor.execute(query, data)
    point_id = cursor.lastrowid
    db.commit()
    cursor.close()
    db.close()

    return make_response(jsonify({'message': 'Point created successfully!', 'point_id': point_id}), 201)

# Get all geo-referenced points
@points.route('/view', methods=['GET'])
@jwt_required()
def get_all_points():
    current_app.logger.info('GET /points route')

    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM GeoReferencedPoints')
    points = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(points), 200

# Get all points for a specific simulation scenario
@points.route('/scenario/<int:scenario_id>', methods=['GET'])
@jwt_required()
def get_points_by_scenario(scenario_id):
    current_app.logger.info(f'GET /points/scenario/{scenario_id} route')

    cursor = db.cursor(dictionary=True)
    query = '''
        SELECT * FROM GeoReferencedPoints WHERE simulation_scenario_id = %s
    '''
    cursor.execute(query, (scenario_id,))
    points = cursor.fetchall()

    cursor.close()
    db.close()

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

    query = '''
        UPDATE GeoReferencedPoints
        SET name = %s, latitude = %s, longitude = %s
        WHERE id = %s
    '''
    data = (name, latitude, longitude, point_id)

    cursor = db.cursor()
    cursor.execute(query, data)
    db.commit()

    if cursor.rowcount == 0:
        cursor.close()
        db.close()
        return jsonify({"error": "Point not found"}), 404

    cursor.close()
    db.close()
    return make_response(jsonify({'message': 'Point updated successfully!'}), 200)

# Delete a geo-referenced point
@points.route('/delete/<int:point_id>', methods=['DELETE'])
@jwt_required()
def delete_point(point_id):
    current_app.logger.info(f'DELETE /points/{point_id} route')

    query = 'DELETE FROM GeoReferencedPoints WHERE id = %s'
    cursor = db.cursor()
    cursor.execute(query, (point_id,))
    db.commit()

    if cursor.rowcount == 0:
        cursor.close()
        db.close()
        return jsonify({"error": "Point not found"}), 404

    cursor.close()
    db.close()
    return make_response(jsonify({'message': 'Point deleted successfully!'}), 200)
