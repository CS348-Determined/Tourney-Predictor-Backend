from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.post("/create_player")
def create_player(player: schemas.PlayerBase, db: Session=Depends(get_db)):
    return crud.create_player(db=db, player=player)

@app.get("/players")
def get_players(db: Session=Depends(get_db)):
    result = db.execute('SELECT * FROM players')
    return result.all()