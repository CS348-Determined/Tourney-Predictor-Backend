from fastapi import HTTPException
from sqlalchemy.orm import Session
import models, schemas

def get_player(db: Session, player_id: int):
    return db.query(models.Player).filter(models.Player.player_id == player_id).first()

def get_team(db: Session, team_id: int):
    return db.query(models.Team).filter(models.Team.team_id == team_id).first()

def create_player(db: Session, player: schemas.PlayerBase):
    db_player = models.Player(**player.dict())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

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

def create_game(db: Session, game: schemas.GameBase):
    db_game = models.Game(**game.dict())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

def update_game(db: Session, game_id: int, game: schemas.GameBase):
    db_game = db.query(models.Game).filter(models.Game.game_id == game_id).first()
    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")
    hero_data = game.dict(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(db_game, key, value)
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

def get_game(db: Session, game_id: int):
    return db.query(models.Game).filter(models.Game.game_id == game_id).first()

def get_all_games(db: Session):
    return db.execute('SELECT * FROM games')