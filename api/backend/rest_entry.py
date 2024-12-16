from flask import Flask

from backend.db_connection import db
import os
from dotenv import load_dotenv

from users.users_routes import users
from teams.teams_routes import teams

def create_app():
    app = Flask(__name__)

    load_dotenv()

    app.config['SECRET_KEY'] = 'someCrazyS3cR3T!Key.!'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_USER'] = os.getenv('DB_USER').strip()
    app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_ROOT_PASSWORD').strip()
    app.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_HOST').strip()
    app.config['MYSQL_DATABASE_PORT'] = int(os.getenv('DB_PORT').strip())
    app.config['MYSQL_DATABASE_DB'] = os.getenv('wireless').strip()

    app.logger.info('current_app(): starting the database connection')
    db.init_app(app)

    app.logger.info('current_app(): registering blueprints with Flask app object.')   
    app.register_blueprint(users,   url_prefix='/users')
    app.register_blueprint(teams,   url_prefix='/teams')

    return app

