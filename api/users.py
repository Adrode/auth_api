from fastapi import APIRouter, Depends
from database import models
from schemas import schemas
from authentication import auth

router = APIRouter()

@router.get('/me', response_model=schemas.User)
def get_me(current_user: models.User = Depends(auth.get_current_user)):
  return current_user