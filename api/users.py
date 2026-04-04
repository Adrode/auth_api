from fastapi import APIRouter, Depends
from database import models
from schemas import schemas
from authentication import short

router = APIRouter()

@router.get('/me', response_model=schemas.User)
def get_me(current_user: models.User = Depends(short.get_current_user)):
  return current_user