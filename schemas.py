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
