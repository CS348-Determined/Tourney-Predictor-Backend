from fastapi import HTTPException
from sqlalchemy.orm import Session
import models, schemas

### PLAYERS ###

def get_player(db: Session, player_id: int):
    return db.query(models.Player).filter(models.Player.player_id == player_id).first()

def create_player(db: Session, player: schemas.PlayerBase):
    db_player = models.Player(**player.dict())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

def update_player(db: Session, player_id: int, team_id: int, name: str):
    db_player = db.query(models.Player).filter(models.Player.player_id == player_id).first()
    if not db_player:
        raise HTTPException(status_code=404, detail="Player not found")
    db_player.team_id = team_id
    db_player.name = name
    db.commit()
    return db_player

def delete_player(db: Session, player_id: int):
    db_player = db.query(models.Player).filter(models.Player.player_id == player_id).first()
    if not db_player:
        raise HTTPException(status_code=404, detail="Player not found")
    db.query(models.Player).filter(models.Player.player_id == player_id).delete()
    db.commit()

### TEAMS ###

def get_team(db: Session, team_id: int):
    return db.query(models.Team).filter(models.Team.team_id == team_id).first()

def update_team(db: Session, team_id: int, team: schemas.TeamBase):
    db_team = db.query(models.Team).filter(models.Team.team_id == team_id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    hero_data = team.dict(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(db_team, key, value)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def create_team(db: Session, team: schemas.TeamBase):
    db_team = models.Team(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def delete_team(db: Session, team_id: int):
    db_team = db.query(models.Team).filter(models.Team.team_id == team_id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    db.query(models.Player).filter(models.Player.team_id == team_id).update({models.Player.team_id: 0}) #players now without team
    db.query(models.Team).filter(models.Team.team_id == team_id).delete()
    db.commit()

### LEAGUE ###
def create_league(db: Session, league: schemas.LeagueBase):
    db_league = models.League(**league.dict())
    db.add(db_league)
    db.commit()
    db.refresh(db_league)
    return db_league

def delete_league(db: Session, league_id: int):
    db_team = db.query(models.League).filter(models.League.league_id == league_id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    db.query(models.Team).filter(models.Team.league_id == league_id).update({models.Team.league_id: 0}) #teams now without league
    db.query(models.League).filter(models.League.league_id == league_id).delete()
    db.commit()

def add_team_to_league(db: Session, league_id: int, team_id: int):
    db_team = db.query(models.Team).filter(models.Team.team_id == team_id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail="team not found")
    db_team.league_id = league_id
    db.commit()
    return db_team

def get_city_by_name(db: Session, name: str):
    return db.query(models.City).filter(models.City.name == name).first()
    
