from pydantic import BaseModel
from sqlalchemy import null

class PlayerBase(BaseModel):
    name: str
    team_id: int
    position_id: int

class Player(PlayerBase):
    player_id: int

    class Config: orm_mode = True

class TeamBase(BaseModel):
    city: str
    name: str
    league_id: int
    record: str #will be it's own type in the future

class Team(BaseModel):
    team_id: int

    class Config:
        orm_mode = True

class LeagueBase(BaseModel):
    name: str

class League(LeagueBase):
    league_id: str

class CityBase(BaseModel):
    name: str
    population: int

class City(CityBase):
    city_id: int

class GameBase(BaseModel):
    home_team_id: int
    away_team_id: int
    winner: int

class Game(GameBase):
    game_id: int

    class Config:
        orm_mode = True
        
class BracketEntryBase(BaseModel):
    team1_id: int
    team2_id: int
    team1_victor: bool
    round: int
    bracket_id: int

class BracketEntry(BracketEntryBase):
    entry_id: int
    class Config:
        orm_mode = True
    
class BracketBase(BaseModel):
    bracket_name: str
    num_rounds: int

class Bracket(BracketBase):
    bracket_id: int
    class Config:
        orm_mode = True
        
class SportBase(BaseModel):
    name: str


class Sport(SportBase):
    sport_id: int
    class Config: orm_mode = True


class PositionBase(BaseModel):
    name: str
    sport_id: int

class Position(PositionBase):
    position_id: int
    class Config: orm_mode = True
