from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

# Create a new Blueprint for teams
teams = Blueprint('teams', __name__)

# Create a new team
@teams.route('/teams', methods=['POST'])
def create_team():
    current_app.logger.info('POST /teams route')
    team_info = request.json
    name = team_info.get('name')
    user_id = team_info.get('user_id')

    if not name or not user_id:
        return jsonify({"error": "Missing required fields"}), 400

    query = '''
        INSERT INTO Teams (name)
        VALUES (%s)
    '''
    cursor = db.cursor()
    cursor.execute(query, (name,))
    team_id = cursor.lastrowid 

    query = '''
        INSERT INTO UserTeams (user_id, team_id)
        VALUES (%s, %s)
    '''
    cursor.execute(query, (user_id, team_id))

    db.commit()
    cursor.close()
    db.close()

    return make_response(jsonify({'message': 'Team created successfully!', 'team_id': team_id}), 201)

# View all teams
@teams.route('/view', methods=['GET'])
def view_teams():
    current_app.logger.info('GET /teams route')

    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Teams')
    teams = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(teams), 200

# Join an existing team
@teams.route('/join', methods=['POST'])
def join_team():
    current_app.logger.info('POST /teams/join route')
    join_info = request.json
    user_id = join_info.get('user_id')
    team_id = join_info.get('team_id')

    if not user_id or not team_id:
        return jsonify({"error": "Missing required fields"}), 400

    cursor = db.cursor()
    query = '''
        SELECT * FROM UserTeams WHERE user_id = %s AND team_id = %s
    '''
    cursor.execute(query, (user_id, team_id))
    membership = cursor.fetchone()

    if membership:
        cursor.close()
        db.close()
        return jsonify({"error": "User is already a member of this team"}), 400

    query = '''
        INSERT INTO UserTeams (user_id, team_id)
        VALUES (%s, %s)
    '''
    cursor.execute(query, (user_id, team_id))

    db.commit()
    cursor.close()
    db.close()

    return make_response(jsonify({'message': 'User successfully joined the team!'}), 200)

# View members of a specific team
@teams.route('/view/<int:team_id>/members', methods=['GET'])
def view_team_members(team_id):
    current_app.logger.info(f'GET /teams/{team_id}/members route')

    cursor = db.cursor(dictionary=True)
    query = '''
        SELECT u.id, u.first_name, u.last_name, u.email 
        FROM Users u
        JOIN UserTeams ut ON u.id = ut.user_id
        WHERE ut.team_id = %s
    '''
    cursor.execute(query, (team_id,))
    members = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(members), 200
