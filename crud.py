from fastapi import HTTPException
from sqlalchemy.orm import Session
import models, schemas

def get_player(db: Session, player_id: int):
    return db.query(models.Player).filter(models.Player.player_id == player_id).first()

def get_team(db: Session, team_id: int):
    return db.query(models.Team).filter(models.Team.team_id == team_id).first()

def create_player(db: Session, player: schemas.PlayerBase):
    db_player = models.Player(**player.dict())
    pos_exist = db.query(models.Position).filter(models.Position.position_id ==db_player.position_id).first()
    if not pos_exist:
        raise HTTPException(status_code=404, detail="Position does not exist")
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
    
def create_bracket(db: Session, defaultTeamId: str, bracket: schemas.BracketBase):
    db_bracket = models.Bracket(**bracket.dict())
    db.add(db_bracket)
    db.commit()
    for i in range(bracket.num_rounds):
        r = i+1
        num_entries = 2 ** (bracket.num_rounds - r)
        for entry in range(num_entries):
            bracketEntry = {
                "round": r,
                "team1_id": defaultTeamId,
                "team2_id":defaultTeamId,
                "bracket_id": db_bracket.bracket_id,
                "team1_victor": True
            }
            db_entry = models.BracketEntry(**bracketEntry)
            print("Adding entry")
            db.add(db_entry)
            
    db.flush()
    db.commit()
    db.refresh(db_bracket)
    return db_bracket.bracket_id

def get_position(db: Session, position_id: int):
    return db.query(models.Player).filter(models.Player.player_id == position_id).first()

def create_position(db: Session, position: schemas.PositionBase):
    db_position = models.Position(**position.dict())
    # sport_exist = db.query(models.Sport).filter(models.Sport.sport_id ==db_position.sport_id).first()
    # if not sport_exist:
    #     raise HTTPException(status_code=404, detail="Sport does not exist")
    db.add(db_position)
    db.commit()
    db.refresh(db_position)
    return db_position

def update_position(db: Session, position_id: int, position: schemas.PositionBase):
    db_position = db.query(models.Position).filter(models.Position.position_id == position_id).first()
    if not db_position:
        raise HTTPException(status_code=404, detail="Position not found")
    hero_data = position.dict(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(db_position, key, value)
    db.add(db_position)
    db.commit()
    db.refresh(db_position)
    return db_position

def create_sport(db: Session, sport: schemas.PositionBase):
    db_sport= models.Sport(**sport.dict())
    db.add(db_sport)
    db.commit()
    db.refresh(db_sport)
    return db_sport
