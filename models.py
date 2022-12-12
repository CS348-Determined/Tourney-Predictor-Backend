from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref
from database import Base

class Player(Base):
    __tablename__ = "players"

    player_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    team_id = Column(Integer, ForeignKey("teams.team_id"))
    position_id = Column(Integer, ForeignKey("positions.position_id"))


class Team(Base):
    __tablename__ = "teams"

    team_id = Column(Integer, primary_key=True, index=True)
    city = Column(String, ForeignKey("cities.name"))
    name = Column(String)
    league_id = Column(Integer, ForeignKey("leagues.league_id"), nullable=True)
    record = Column(String)

class League(Base):
    __tablename__ = "leagues"

    league_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    sport_id = Column(Integer, ForeignKey("sports.sport_id"))


class City(Base):
    __tablename__ = "cities"

    city_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    population = Column(Integer)

class Game(Base):
    __tablename__ = "games"

    game_id = Column(Integer, primary_key=True, index=True)
    home_team_id = Column(Integer, ForeignKey("teams.team_id"))
    away_team_id = Column(Integer, ForeignKey("teams.team_id"))
    winner = Column(Integer, index=True, nullable=True, default=-1)

class Bracket(Base):
    __tablename__ = "brackets"
    bracket_id = Column(Integer, primary_key=True, index=True)
    bracket_name = Column(String, index=True, unique=True)
    num_rounds = Column(Integer)
class BracketEntry(Base):
    __tablename__ = "bracket_entries"
    entry_id = Column(Integer, primary_key=True, index=True)
    team1_id = Column(Integer, ForeignKey("teams.team_id"), nullable=False)
    team2_id = Column(Integer, ForeignKey("teams.team_id"), nullable=False)
    team1_victor = Column(String, index=True)
    round = Column(Integer)
    bracket_id = Column(Integer, ForeignKey("brackets.bracket_id"), nullable=False)

class Sport(Base):
    __tablename__ = "sports"

    sport_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

class Position(Base):
    __tablename__ = "positions"

    position_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    sport_id = Column(Integer, ForeignKey("sports.sport_id"))
