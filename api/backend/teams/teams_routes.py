from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

from backend.db_files.models import Team
from backend.db_files.models import User
from backend.db_files.database import db_session
from sqlalchemy import update

from flask_jwt_extended import jwt_required

# Create a new Blueprint for teams
teams = Blueprint('teams', __name__)

# Create a new team
@teams.route('/create', methods=['POST'])
@jwt_required()
def create_team():
    current_app.logger.info('POST /teams route')
    team_info = request.json
    name = team_info.get('name')
    user_id = team_info.get('user_id')

    if not name or not user_id:
        return jsonify({"error": "Missing required fields"}), 400

    team = Team(name=name)
    db_session.add(team)
    db_session.commit()

    team_id = Team.query.filter_by(name=name).first().id
    user = User.query.filter_by(id=user_id).first()
    user.team_id = team_id
    db_session.commit()

    return make_response(jsonify({'message': 'Team created successfully!', 'team_id': team_id}), 201)

# View all teams
@teams.route('/view', methods=['GET'])
@jwt_required()
def view_teams():
    current_app.logger.info('GET /teams route')

    teams = Team.query.all()
    teams_dict = [team.as_dict() for team in teams]

    return jsonify(teams_dict), 200

# Join an existing team
@teams.route('/join', methods=['POST'])
@jwt_required()
def join_team():
    current_app.logger.info('POST /teams/join route')
    join_info = request.json
    user_id = join_info.get('user_id')
    team_id = join_info.get('team_id')

    team = Team.query.filter_by(id=team_id).first()
    if not team:
        return jsonify({"error": "Team not found", "team_id": team_id}), 404

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"error": "User not found", "user_id": user_id}), 404

    updated = update(User).where(User.id == user_id).values({"team_id": team_id})
    db_session.execute(updated)
    db_session.commit()

    return make_response(jsonify({'message': 'User successfully joined the team!'}), 200)

# View members of a specific team
@teams.route('/view/<int:team_id>/members', methods=['GET'])
@jwt_required()
def view_team_members(team_id):
    current_app.logger.info(f'GET /teams/{team_id}/members route')

    members = User.query.filter_by(team_id=team_id).all()
    members_dict = [member.as_dict() for member in members]

    return jsonify(members_dict), 200
