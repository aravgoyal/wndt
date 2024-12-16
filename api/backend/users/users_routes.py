from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
import hashlib
from backend.db_connection import db

# Create a new Blueprint for users
users = Blueprint('users', __name__)

# Utility function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register a new user
@users.route('/register', methods=['POST'])
def add_user():
    current_app.logger.info('POST /users route')
    user_info = request.json
    first_name = user_info.get('first_name')
    last_name = user_info.get('last_name')
    email = user_info.get('email')
    password = user_info.get('password')
    
    if not email or not password or not first_name or not last_name:
        return jsonify({"error": "Missing required fields"}), 400

    hashed_password = hash_password(password)

    query = '''
        INSERT INTO Users (first_name, last_name, email, password)
        VALUES (%s, %s, %s, %s)
    '''
    data = (first_name, last_name, email, hashed_password)
    cursor = db.cursor()
    cursor.execute(query, data)
    db.commit()
    cursor.close()
    db.close()

    return make_response(jsonify({'message': 'User added successfully!'}), 201)

# Login user
@users.route('/login', methods=['POST'])
def login_user():
    current_app.logger.info('POST /login route')
    user_info = request.json
    email = user_info.get('email')
    password = user_info.get('password')

    if not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Users WHERE email = %s', (email,))
    user = cursor.fetchone()
    
    if user and user['password'] == hash_password(password):
        cursor.close()
        db.close()
        return make_response(jsonify({"message": "Login successful!", "user_id": user['id']}), 200)
    
    cursor.close()
    db.close()
    return jsonify({"error": "Invalid email or password"}), 401

# Route to get user by ID (for example purposes)
@users.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Users WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    
    if user:
        cursor.close()
        db.close()
        return jsonify(user), 200
    
    cursor.close()
    db.close()
    return jsonify({"error": "User not found"}), 404
