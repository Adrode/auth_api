from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Annotated
from database import get_db
import models, schemas, auth

router = APIRouter()

session_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", response_model=schemas.User)
def register(
  data: schemas.CreateUser,
  db: session_dependency
  ):
  try:
    user = models.User(
      email=data.email,
      hashed_password=auth.hash_password(data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user
  except IntegrityError:
    raise HTTPException(
      status_code=400,
      detail="Bad request"
    )

@router.get("/", response_model=list[schemas.User])
def get_users(db: session_dependency):
  users = db.query(models.User).all()

  if not users:
    raise HTTPException(
      status_code=400
    )
  
  return users 