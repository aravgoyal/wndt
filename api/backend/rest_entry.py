from flask import Flask

from backend.db_connection import db
import os
from dotenv import load_dotenv
from backend.db_files.database import init_db

from backend.users.users_routes import users
from backend.teams.teams_routes import teams
from backend.scenarios.scenarios_routes import scenarios
from backend.points.points_routes import points

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from datetime import timedelta

def create_app():
    app = Flask(__name__)

    load_dotenv()

    app.config['SECRET_KEY'] = 'W!0TS3CReTk3Y.!'
    jwt = JWTManager(app)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_USER'] = os.getenv('DB_USER')
    app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_ROOT_PASSWORD')
    app.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_HOST')
    app.config['MYSQL_DATABASE_PORT'] = int(os.getenv('DB_PORT'))
    app.config['MYSQL_DATABASE_DB'] = os.getenv('wireless')

    app.logger.info('current_app(): starting the database connection')
    db.init_app(app)
    init_db()

    app.logger.info('current_app(): registering blueprints with Flask app object.')   
    app.register_blueprint(users,     url_prefix='/users')
    app.register_blueprint(teams,     url_prefix='/teams')
    app.register_blueprint(scenarios, url_prefix='/scenarios')
    app.register_blueprint(points,    url_prefix='/points')

    return app

