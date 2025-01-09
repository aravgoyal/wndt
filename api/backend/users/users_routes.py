from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

import hashlib
from backend.db_connection import db
from backend.db_files.database import db_session
from backend.db_files.models import User
from sqlalchemy.exc import IntegrityError

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

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=hashed_password
    )

    try:
        db_session.add(new_user)
        db_session.commit()
        return make_response(jsonify({'message': 'User added successfully!'}), 201)
    except IntegrityError:
        db_session.rollback()
        return jsonify({"error": "Email already exists"}), 409
    except Exception as e:
        current_app.logger.error(f"Error adding user: {e}")
        db_session.rollback()
        return jsonify({"error": "An error occurred while adding the user"}), 500

# Login user
@users.route('/login', methods=['POST'])
def login_user():
    current_app.logger.info('POST /login route')
    user_info = request.json
    email = user_info.get('email')
    password = user_info.get('password')

    if not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    user = User.query.filter_by(email=email).first()
    
    if user and user.password == hash_password(password):
        access_token = create_access_token(identity=email)
        return make_response(jsonify({"message": "Login successful!", "access_token": access_token}), 200)
    
    return jsonify({"error": "Invalid email or password"}), 401

# Get user info
@users.route('/view/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    
    if user:
        return jsonify(user.as_dict()), 200
    
    return jsonify({"error": "User not found"}), 404

# Get all user info
@users.route('/view', methods=['GET'])
@jwt_required()
def get_all_users():
    users = User.query.all()
    users_dict = [user.as_dict() for user in users]
    return jsonify(users_dict), 200
