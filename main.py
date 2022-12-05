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

@app.get("/league/{leagueId}")
def get_league(leagueId: str, db: Session=Depends(get_db)):
    result = db.execute('SELECT * FROM leagues WHERE league_id = '+leagueId)
    return result.all()

@app.put("/updateTeam/{teamId}")
def update_team(team: schemas.TeamBase, teamId: str, db: Session=Depends(get_db)):
    return crud.update_team(db=db, team_id=teamId, team=team)

@app.post("/addTeam")
def create_team(team: schemas.TeamBase, db: Session=Depends(get_db)):
    return crud.create_team(db=db, team=team)