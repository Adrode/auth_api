from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models

app = FastAPI()

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
  users = db.query(models.User).all()

  if not users:
    raise HTTPException(
      status_code=400
    )
  
  return users 