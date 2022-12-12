from turtle import position
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
import crud, models, schemas
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

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

@app.post("/create_player")
def create_player(player: schemas.PlayerBase, db: Session=Depends(get_db)):
    return crud.create_player(db=db, player=player)

@app.get("/players")
def get_players(db: Session=Depends(get_db)):
    result = db.execute('SELECT * FROM players')
    return result.all()

@app.get("/team/{teamId}")
def get_team(teamId: str, db: Session=Depends(get_db)):
    result = db.execute('SELECT * FROM teams WHERE team_id = '+teamId)
    return result.all()

@app.get("/allTeams")
def get_players(db: Session=Depends(get_db)):
    result = db.execute('SELECT * FROM teams')
    return result.all()

@app.get("/league/{leagueId}")
def get_league(leagueId: str, db: Session=Depends(get_db)):
    result = db.execute('SELECT * FROM leagues WHERE league_id = '+leagueId)
    return result.all()

@app.put("/updateTeam/{teamId}")
def update_team(team: schemas.TeamBase, teamId: str, db: Session=Depends(get_db)):
    return crud.update_team(db=db, team_id=teamId, team=team)

@app.put("/updateBracketEntry/{entryId}")
def update_bracketEntry(bracketEntry: schemas.BracketEntryBase, entryId: str, db: Session=Depends(get_db)):
    query = ("UPDATE bracket_entries set team1_id = "+ str(bracketEntry.team1_id) + ", "
        "team2_id = " + str(bracketEntry.team2_id) + ", "
        "team1_victor = " + str(bracketEntry.team1_victor) + ", "
        "round = " + str(bracketEntry.round) + ", "
        "bracket_id = " + str(bracketEntry.bracket_id) + " "
        "WHERE entry_id = " + str(entryId)+";")
    #print(query)
    result = db.execute(query)
    db.commit()
    #return result.all()

@app.get("/getBracketEntries/{bracketId}")
def get_team(bracketId: str, db: Session=Depends(get_db)):
    result = db.execute('SELECT * FROM bracket_entries WHERE bracket_id = '+bracketId+' ORDER BY entry_id')
    return result.all()

@app.get("/getPlayersForTeam/{teamId}")
def get_team(teamId: str, db: Session=Depends(get_db)):
    result = db.execute('SELECT * FROM players WHERE team_id = '+teamId)
    return result.all()

@app.get("/bracket/{bracketId}")
def get_team(bracketId: str, db: Session=Depends(get_db)):
    result = db.execute('SELECT * FROM brackets WHERE bracket_id = '+bracketId)
    return result.all()

@app.post("/addTeam")
def create_team(team: schemas.TeamBase, db: Session=Depends(get_db)):
    return crud.create_team(db=db, team=team)

@app.post("/addGame")
def create_game(game: schemas.GameBase, db: Session=Depends(get_db)):
    return crud.create_game(db=db, game=game)

@app.put("/updateGame/{gameId}")
def update_game(game: schemas.GameBase, gameId: str, db: Session=Depends(get_db)):
    return crud.update_game(db=db, game_id=gameId, game=game)

@app.get("/game/{gameId}")
def get_game(gameId: str, db: Session=Depends(get_db)):
    result = db.execute('SELECT * FROM games WHERE game_id = '+gameId)
    return result.all()
    
@app.post("/addBracket/{defaultTeamId}")
def create_team(defaultTeamId:str, bracket: schemas.BracketBase, db: Session=Depends(get_db)):
    return crud.create_bracket(db=db, defaultTeamId=defaultTeamId,bracket=bracket)

@app.get("/allLeagues")
def get_allLeagues(db: Session=Depends(get_db)):
    result = db.execute('SELECT * FROM leagues')
    return result.all()

@app.get("/position/{positionId}")
def get_position(positionId: str, db: Session=Depends(get_db)):
    result = db.execute('SELECT * from players where players.position_id = '+positionId)
    return result.all()
# def get_position(positionName: str, db: Session=Depends(get_db)):
#     result = db.execute('SELECT players.player_id, players.name, players.team_id, players.position_id FROM players join positions on players.position_id = positions.position_id WHERE positions.name = '+positionName)
#     return result.all()


@app.post("/addPosition")
def create_position(position: schemas.PositionBase, db: Session=Depends(get_db)):
    return crud.create_position(db=db, position=position)

@app.put("/updatePosition/{positionId}")
def update_position(position: schemas.PositionBase, positionId: str, db: Session=Depends(get_db)):
    return crud.update_position(db=db, position_id=positionId, position=position)

@app.post("/addSport")
def create_sport(sport: schemas.SportBase, db: Session=Depends(get_db)):
    return crud.create_sport(db=db, sport=sport)

@app.get("/sport/{positionId}")
def get_sport_from_position_id(positionId: str, db: Session=Depends(get_db)):
    result = db.execute('SELECT sports.name FROM positions inner join sports on positions.sport_id = sports.sport_id WHERE positions.position_id = '+positionId)
    return result.all()
