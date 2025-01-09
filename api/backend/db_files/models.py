from sqlalchemy import Column, Integer, String, ForeignKey
from geoalchemy2 import Geometry
from backend.db_files.database import Base
from flask_sqlalchemy import SQLAlchemy

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False) 
    last_name = Column(String(50))
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'))

    def __init__(self, first_name=None, last_name=None, email=None, password=None, team_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.team_id = team_id

    def __repr__(self):
        return f'<User {self.first_name!r}>'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Team(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return f'<Team {self.name!r}>'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Scenario(Base):
    __tablename__ = 'scenarios'
    id = Column(Integer, primary_key=True)
    visibility = Column(String(50), nullable=False)
    frequency = Column(String(50))
    scenario_type = Column(String(50))
    map_center = Column(SQLAlchemy().JSON)
    map_size = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self, visibility=None, frequency=None, scenario_type=None, map_center=None, map_size=None, user_id=None):
        self.visibility = visibility
        self.frequency = frequency
        self.scenario_type = scenario_type
        self.map_center = map_center
        self.map_size = map_size
        self.user_id = user_id

    def __repr__(self):
        return f'<Scenario {self.id!r}>'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class GeoPoint(Base):
    __tablename__ = 'points'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    geom = Column(SQLAlchemy().JSON)
    scenario_id = Column(Integer, ForeignKey('scenarios.id'))

    def __init__(self, name=None, geom=None, scenario_id=None):
        self.name = name
        self.geom = geom
        self.scenario_id = scenario_id

    def __repr__(self):
        return f'<Point {self.name!r}>'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}