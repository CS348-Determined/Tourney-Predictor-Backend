from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
import crud, models, schemas
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import math

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

### PLAYERS ###

@app.post("/createPlayer")
def create_player(player: schemas.PlayerBase, db: Session=Depends(get_db)):
    return crud.create_player(db=db, player=player)


class PlayerReturn(BaseModel):
    name: str
    team: str
    team_id: int
    league: str
    league_id: int

@app.get("/getPlayer/{player_id}")
def view_player(player_id: str, db: Session=Depends(get_db)):
    result = db.execute('SELECT * FROM players WHERE player_id = ' + player_id).first()
    if result.team_id != 0:
        team = db.execute('SELECT * FROM teams WHERE team_id = ' + str(result.team_id)).first()
        league = db.execute('SELECT * FROM leagues WHERE league_id = ' + str(team.league_id)).first()
        player = PlayerReturn(name=result.name, team=team.city + " " + team.name, team_id=result.team_id, league=league.name, league_id=team.league_id)
        return player
    else:
        player = PlayerReturn(name=result.name, team="Free Agent", team_id=-1, league="Player not in league", league_id=-1)
        return player
    
class PlayerUpdate(BaseModel):
    new_name: str
    new_team_id: int
    player_id: int  

@app.put("/updatePlayer")
def edit_player(newinfo: PlayerUpdate, db: Session=Depends(get_db)):
    crud.update_player(db=db, player_id=newinfo.player_id, team_id=newinfo.new_team_id, name=newinfo.new_name)
    message = {"Player updated successfully"}
    return message

@app.delete("/deletePlayer/{player_id}")
def delete_player(player_id: int, db: Session=Depends(get_db)):
    crud.delete_player(db=db, player_id=player_id)
    message = {"player deleted successfully"}
    return message

@app.get("/players")
def get_players(db: Session=Depends(get_db)):
    result = db.execute('SELECT * FROM players')
    return result.all()

### TEAMS ###

@app.get("/teams")
def get_teams(db: Session=Depends(get_db)):
    result = db.execute('SELECT * FROM teams')
    return result.all()

@app.get("/team/{teamId}")
def get_team(teamId: str, db: Session=Depends(get_db)):
    result = db.execute('SELECT * FROM teams WHERE team_id = '+teamId)
    return result.all()

@app.put("/updateTeam/{teamId}")
def update_team(team: schemas.TeamBase, teamId: str, db: Session=Depends(get_db)):
    return crud.update_team(db=db, team_id=teamId, team=team)

@app.post("/createTeam")
def create_team(team: schemas.TeamBase, db: Session=Depends(get_db)):
    return crud.create_team(db=db, team=team)

@app.delete("/deleteTeam/{team_id}")
def delete_team(team_id: int, db: Session=Depends(get_db)):
    crud.delete_team(db=db, team_id=team_id)
    message = {"team deleted successfully"}
    return message

### LEAGUES ###

@app.get("/league/{leagueId}")
def get_league(leagueId: str, db: Session=Depends(get_db)):
    league = db.execute('SELECT * FROM leagues WHERE league_id = '+leagueId).all()
    teams = db.execute('SELECT * FROM teams WHERE league_id = '+leagueId).all()
    return [league, teams]

@app.post("/createLeague")
def create_league(league: schemas.LeagueBase, db: Session=Depends(get_db)):
    return crud.create_league(db=db, league=league)

@app.delete("/deleteLeague/{league_id}")
def delete_league(league_id: int, db: Session=Depends(get_db)):
    crud.delete_league(db=db, league_id=league_id)
    message = {"league deleted successfully"}
    return message

@app.put("/addTeamToLeague/{league_id}")
def add_team_to_league(league_id: int, team_id: int, db: Session=Depends(get_db)):
    crud.add_team_to_league(db=db, league_id=league_id, team_id=team_id)
    message = {"team added to league"}
    return message

#rivalry

class Bod(BaseModel):
    target: int

@app.get("/teamsWithinRange")
def get_teams_within_range(team_id: int, target: int, db: Session=Depends(get_db)):
    team = db.execute('SELECT * FROM teams WHERE team_id = ' + str(team_id)).first()
    if (team.league_id < 1 or not team.league_id ):
        return None
    league_teams = db.execute('SELECT * FROM teams WHERE league_id = ' + str(team.league_id)).all()
    rivals = []
    teamcity = crud.get_city_by_name(db=db, name=team.city)
    if not teamcity:
        return {"uh oh"}
    for ateam in league_teams:
        acity = crud.get_city_by_name(db=db, name=ateam.city)
        dist_degrees = math.sqrt((acity.lat - teamcity.lat)**2 + (acity.lng - teamcity.lng)**2)
        dist = dist_degrees * 69.4
        if (target > dist) & (acity.city_id != teamcity.city_id):
            rivals.append(ateam)
    return rivals